from ultralytics import YOLO
import cv2
import cvzone
import random
# import math
import json
import os
import requests
import subprocess
from time import time, sleep
import io
import os
import base64
import threading
from datetime import datetime
import uuid

from collections import Counter
import pyrebase
from gpiozero import Button

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

subprocess.call(['espeak', '-s', '150', "Welcome to smart vision hat"])

firebaseConfig = {
  'apiKey': "AIzaSyCQAj14X510dN2LreUiVJ-Ox26wqkR_xX8",
  'authDomain': "smart-vision-hat.firebaseapp.com",
  'projectId': "smart-vision-hat",
  'storageBucket': "smart-vision-hat.appspot.com",
  'messagingSenderId': "627181110284",
  'appId': "1:627181110284:web:deb55084063000eb565a29",
  'measurementId': "G-LL0X4KC7S6",
  'databaseURL': 'https://smart-vision-hat-default-rtdb.asia-southeast1.firebasedatabase.app'
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

device_id = "b8:27:eb:a8:66:d1"

button2 = Button(2)
button3 = Button(3)
button4 = Button(18)

button2_state = False
button3_state = False
button4_state = False

eyes_on_mode = False
interval = 20

START = time()

server_ip = "https://misoto22.pythonanywhere.com"
# server_ip = "http://127.0.0.1:5000"
# Define the URL of your Flask API endpoint
api_url = f"{server_ip}/api/upload"
api_url_process = f"{server_ip}/api/process"
api_url_email = f"{server_ip}/api/send_email"

with open('./config.json') as config_file:
    config = json.load(config_file)

cap = cv2.VideoCapture(config["videoCapture"]["device"])
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["videoCapture"]["width"])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["videoCapture"]["height"])

model = YOLO(config["paths"]["model_Path"])

classNames = config["classes"]["classNames"]

def make_dict(items):
    d = {}
    for item in items:
        d[item] = d.get(item, 0) + 1

    return d

def combine_items(items):
    # Count the occurrences of each item
    item_counts = Counter(items)

    # Initialize an empty list to store the formatted strings
    formatted_items = []

    # Iterate through the item counts and create the formatted strings
    for item, count in item_counts.items():
        if count == 1:
            formatted_items.append(f'1 {item}')
        else:
            formatted_items.append(f'{count} {item}s')

    return formatted_items


def sub_speak(item):
    subprocess.call(['espeak', '-s', '150', item])

def speak_single(item):
    # Initialize the gTTS object with the text 
    sub_speak(item)


def speak(items):
    for item in items:
        text = f"{item}"
        speak_single(text)


def detect_image(frame):
    # Get the current timestamp
    current_time = datetime.now()
    detection_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    detection_mode = "Eyes-on" if eyes_on_mode else "Insight-snap"

    processing_location = "Cloud"


    _, frame_jpeg = cv2.imencode(".jpg", frame)
    image_data_base64 = base64.b64encode(frame_jpeg.tobytes()).decode('utf-8')

    items = []
    # Call Flask API endpoint to send both frame and speak data
    try:
        payload = {
            "image": image_data_base64,
        }
        headers = {"Content-Type": "application/json"}  # Specify JSON content type

        response = requests.post(api_url_process, data=json.dumps(payload), headers=headers, timeout=20)
    
        if (response.status_code == 200):
            # print(response.status_code)
            resonse_data = json.loads(response.text)
            response_labels = resonse_data['labels']
            items = response_labels
            image_data = resonse_data['image']
            filename = str(uuid.uuid4())
            if image_data:
            # Ensure the 'temp' directory exists
                if not os.path.exists('temp'):
                    os.makedirs('temp')
                
                # Save the image temporarily
                file_path = os.path.join("temp", filename)
                image_data_bytes = base64.b64decode(image_data.encode('utf-8'))
                with open(file_path, 'wb') as image_file:
                    image_file.write(image_data_bytes)


            frame = cv2.imread(file_path)

            # print(labels)

            os.remove(file_path) # Delete the temp file


        else:
            processing_location = "On-device"
            results = model(frame, stream=False)

            for r in results:
                boxes = r.boxes

                for box in boxes:
                    # Bounding box

                    x1, y1, x2, y2 = box.xyxy[0]
                    w, h = int(x2) - int(x1), int(y2) - int(y1)
                    bbox = int(x1), int(y1), int(w), int(h)


                    conff = round(float(box.conf[0]), 2)
                    if (conff >= 0.4):
                        cvzone.cornerRect(frame, bbox, l=config["rectSetup"]["length"], t=config["rectSetup"]["thickness"],
                                            colorR=tuple(config["rectSetup"]["rectColor"]))
                        # Class name
                        cls = box.cls[0]
                        crClass = classNames[int(cls)]
                        cvzone.putTextRect(frame, f'{crClass} {conff}', (max(0, int(x1)), max(35, int(y1))),
                                            scale=config["textSetup"]["scale"], thickness=config["textSetup"]["thickness"],
                                            offset=config["textSetup"]["offset"])

                        items.append(crClass)

    except Exception as e:
        print(f"Error: {str(e)}")

    # cv2.imshow('Captured', frame)
    speak_single(f"{len(items)} item{'s' if not len(items) == 1 else ''} detected")
    items_dict = make_dict(items)
    items = combine_items(items)
    speak(items)
    
    send_data_thread = threading.Thread(target=send_data, args=(frame, items_dict, detection_time, detection_mode, processing_location))
    send_data_thread.start()

    
    
def send_data(frame, items_dict, detection_time, detection_mode, processing_location):
    # call flask url endpoint
    # Convert the frame to JPEG format
    _, frame_jpeg = cv2.imencode(".jpg", frame)
    items_json = json.dumps(items_dict)
    image_data_base64 = base64.b64encode(frame_jpeg.tobytes()).decode('utf-8')

    # Call Flask API endpoint to send both frame and speak data
    try:
        payload = {
            "device_id": device_id,
            "image": image_data_base64,
            "labels": items_json,
            "timestamp": detection_time,
            "mode": detection_mode,
            "processing_location": processing_location
        }
        headers = {"Content-Type": "application/json"}  # Specify JSON content type

        response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=10)
            
    except Exception as e:
        print(f"Error: {str(e)}")


def capture_image():
    global eyes_on_mode
    global START
    START = time()
    while eyes_on_mode:
        device_data = db.child("devices").child(device_id).get()
        if 'privacy' in device_data.val():
            device_data = device_data.val()
            interval = device_data['refresh_rate']
        else:
            interval = 20

        # Capture the image using your camera logic
        print(f"Interval: {time() - START}")
        start = time()
        detected_frame = cv2.flip(frame, 0)
        detect_image(detected_frame)
        print(f"Detection: {time() - start}")
        # Sleep for 10 seconds
        START = time()
        sleep(interval)
        
def send_email():
    sg = SendGridAPIClient('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')
    email = Mail(
        from_email='mlfdb2023@gmail.com',
        to_emails='cxw8848@hotmail.com', #'smartvisionhat@gmail.com',
        subject='Emergency Alert from Smart Vision Hat',
        html_content='<strong>You have a new alert from your contact \n sent by Smart Vision Hat</strong>'
    )
    response = sg.send(email)
    print(response.status_code)
    
ready = False
if __name__ == '__main__':
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Display the frame in a window
        cv2.imshow('Camera Feed', frame)

        # Check if the 'c' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if not ready:
            speak_single("Ready")
            ready = True
        

        if button2.is_pressed and not button2_state:
            button2_state = True

        if button3.is_pressed and not button3_state:
            button3_state = True

        if button4.is_pressed and not button4_state:
            button4_state = True

        if button2.is_pressed == False and button2_state and not eyes_on_mode:
        # if key == ord('c') and not eyes_on_mode:
            button2_state = False
            detected_frame = cv2.flip(frame, 0)
            detect_image(detected_frame)

        if button3.is_pressed == False and button3_state:
        # if key == ord('d'):
            button3_state = False
            eyes_on_mode = not eyes_on_mode
            if eyes_on_mode:
                image_capture_thread = threading.Thread(target=capture_image)
                image_capture_thread.start()

        if button4.is_pressed == False and button4_state:
            send_email()
            
        # if key == ord('e'):
        #     try:
        #         payload = {
        #             "device_id": device_id,
        #         }
        #         headers = {"Content-Type": "application/json"}  # Specify JSON content type

        #         response = requests.post(api_url_email, data=json.dumps(payload), headers=headers, timeout=10)
                        
            # except Exception as e:
            #     print(f"Error: {str(e)}")
        

        # Check if the 'q' key is pressed to quit the program
        if key == ord('q'):
            eyes_on_mode = False
            break

    # Release the camera and close all OpenCV windows
    eyes_on_mode = False
    cap.release()
    cv2.destroyAllWindows()
