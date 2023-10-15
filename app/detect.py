from flask import Blueprint, jsonify, request
import os
import pyrebase
import json
import uuid
from PIL import Image
import base64
import cvzone
from ultralytics import YOLO
import cv2

# Get the directory of the currently executing script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the name of your JSON configuration file
config_file_name = 'config.json'

# Create the absolute path to the JSON configuration file
config_file_path = os.path.join(current_directory, config_file_name)

# Load the JSON configuration file

with open(config_file_path) as config_file:
    config = json.load(config_file)

model = YOLO(config["paths"]["model_Path"])
classNames = config["classes"]["classNames"]
api_bp = Blueprint('api', __name__, url_prefix='/api')

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





def detect_image(frame):

    # return (frame, ['person'])

    results = model(frame, stream=False)
    items = []

    try:

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
            print(f"error {e}")

            return jsonify({'message': str(e)}), 500        

    return (frame, items)


file_path = "./cat_dog.jpg"

frame = cv2.imread(file_path)

frame, labels = detect_image(frame)
# labels = ["Person"]

# print(labels)

print(labels)

# Convert labels (an array) to a list

# Prepare a JSON response with image data and labels

# Return the JSON response
print("success")
