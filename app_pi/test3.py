from ultralytics import YOLO
import cv2
import cvzone
import random
# import math
import json
import os
import requests
import subprocess
from time import sleep
import io
import os
import base64
import threading

from collections import Counter
import pyrebase
from gpiozero import Button

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
counter = 1
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

device_id = "b8:27:eb:a8:66:d1"

button2 = Button(2, bounce_time=2)
button3 = Button(3, bounce_time=2)

button2_state = False
button3_state = False

eyes_on_mode = False
interval = 20

server_ip = "172.20.10.4:5000"
# Define the URL of your Flask API endpoint
api_url = f"http://{server_ip}/api/upload"


with open('config.json') as config_file:
    config = json.load(config_file)

cap = cv2.VideoCapture(config["videoCapture"]["device"])
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["videoCapture"]["width"])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["videoCapture"]["height"])

model = YOLO(config["paths"]["model_Path"])

classNames = config["classes"]["classNames"]


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
        print(text)


def detect_image(frame):
    global counter
    print(f"detect {counter}")
    counter+=1

detecting_state = False

def capture_image():
    global eyes_on_mode
    global detecting_state
    while eyes_on_mode:

        # Capture the image using your camera logic
        detected_frame = cv2.flip(frame, 0)
        detect_image(detected_frame)
        detecting_state = True
        # Sleep for 10 seconds
        
        sleep(5)
        detecting_state = False

ready = False
if __name__ == '__main__':
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Display the frame in a window
        # cv2.imshow('Camera Feed', frame)

        # Check if the 'c' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if not ready:
            speak_single("Ready")
            ready = True
        if button2.is_pressed and not button2_state:
            button2_state = True
        
        if button3.is_pressed and not button3_state:
            button3_state = True           
        
        if button2.is_pressed == False and button2_state and not eyes_on_mode:
            button2_state = False
            print(f"hello {counter}")
            counter+=1
            detected_frame = cv2.flip(frame, 0)
            detect_image(detected_frame)

        if button3.is_pressed == False and button3_state:
            button3_state = False
            eyes_on_mode = not eyes_on_mode
            if eyes_on_mode:
                print(eyes_on_mode)
                
                image_capture_thread = threading.Thread(target=capture_image)
                image_capture_thread.start()
                #capture_image()
        

        # Check if the 'q' key is pressed to quit the program
        if key == ord('q'):
            eyes_on_mode = False
            break

    # Release the camera and close all OpenCV windows
    eyes_on_mode = False
    cap.release()
    cv2.destroyAllWindows()

