from ultralytics import YOLO
import cv2
import cvzone
import random
# import math
import json
import os
import requests


from gtts import gTTS
import io
import os
import pygame
import base64

from gpiozero import Button
button = Button(2)

server_ip = "127.0.0.1:5000"
# Define the URL of your Flask API endpoint
api_url = f"http://{server_ip}/api/upload"


with open('config.json') as config_file:
    config = json.load(config_file)

cap = cv2.VideoCapture(config["videoCapture"]["device"])
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["videoCapture"]["width"])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["videoCapture"]["height"])

model = YOLO(config["paths"]["model_Path"])

classNames = config["classes"]["classNames"]

def speak(items):
    # Text you want to convert to speech
    text = f"{len(items)} item{'s' if not len(items) == 1 else ''} detected"

    # Initialize the gTTS object with the text and language (e.g., 'en' for English)
    tts = gTTS(text=text, lang='en')

    # Convert the speech to an in-memory file-like object
    speech_file = io.BytesIO()
    tts.write_to_fp(speech_file)
    speech_file.seek(0)

    # Initialize pygame to play the speech
    pygame.mixer.init()
    pygame.mixer.music.load(speech_file)

    # Play the speech
    pygame.mixer.music.play()

    # Wait for the speech to finish
    while pygame.mixer.music.get_busy():
        pass

    for item in items:
        text = f"{item}"

        # Initialize the gTTS object with the text and language (e.g., 'en' for English)
        tts = gTTS(text=text, lang='en')

        # Convert the speech to an in-memory file-like object
        speech_file = io.BytesIO()
        tts.write_to_fp(speech_file)
        speech_file.seek(0)

        # Initialize pygame to play the speech
        pygame.mixer.init()
        pygame.mixer.music.load(speech_file)

        # Play the speech
        pygame.mixer.music.play()

        # Wait for the speech to finish
        while pygame.mixer.music.get_busy():
            pass


def detect_image(frame):
    results = model(frame, stream=False)
    items = []

    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Bounding box

            x1, y1, x2, y2 = box.xyxy[0]
            w, h = int(x2) - int(x1), int(y2) - int(y1)
            bbox = int(x1), int(y1), int(w), int(h)


            cvzone.cornerRect(frame, bbox, l=config["rectSetup"]["length"], t=config["rectSetup"]["thickness"],
                                colorR=tuple(config["rectSetup"]["rectColor"]))


            conff = round(float(box.conf[0]), 2)
            if (conff >= 0.4):
                # Class name
                cls = box.cls[0]
                crClass = classNames[int(cls)]
                cvzone.putTextRect(frame, f'{crClass} {conff}', (max(0, int(x1)), max(35, int(y1))),
                                    scale=config["textSetup"]["scale"], thickness=config["textSetup"]["thickness"],
                                    offset=config["textSetup"]["offset"])

                items.append(crClass)

    # cv2.imshow('Captured', frame)
    speak(items)
    # call flask url endpoint
    # Convert the frame to JPEG format
    _, frame_jpeg = cv2.imencode(".jpg", frame)
    items_json = json.dumps(items)
    image_data_base64 = base64.b64encode(frame_jpeg.tobytes()).decode('utf-8')

    # Call Flask API endpoint to send both frame and speak data
    try:
        payload = {
            "device_id": "1",
            "image": image_data_base64,
            "labels": items_json
        }
        headers = {"Content-Type": "application/json"}  # Specify JSON content type

        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    
    except Exception as e:
        print(f"Error: {str(e)}")



if __name__ == '__main__':
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Display the frame in a window
        cv2.imshow('Camera Feed', frame)

        # Check if the 'c' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if not ready:
            print("Ready")
            ready = True
        if button.is_pressed:
            detect_image(frame)

        # Check if the 'q' key is pressed to quit the program
        if key == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
