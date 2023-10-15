from flask import Blueprint, jsonify, request, current_app
import os
import pyrebase
import json
import uuid
from PIL import Image
import base64
import cvzone
from ultralytics import YOLO
import cv2
import threading
import queue


result_queue = queue.Queue()

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

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


@api_bp.route('/upload', methods=['POST'])
def upload():
    try:
        # Get data from the request JSON
        data = request.get_json()

        # Extract device_id, image data, and items list from the JSON
        device_id = data.get('device_id')
        image_data = data.get('image')
        time_data = data.get('timestamp')
        mode_data = data.get('mode')
        processing_data = data.get('processing_location')
        labels_json = data.get('labels', {})
        labels = json.loads(labels_json)
        private = False
        filename = str(uuid.uuid4())

        print(labels)

        # Check if device_id is provided
        if device_id is None:
            return jsonify({'message': 'Device ID is required'}), 400
        
        device_data = db.child("devices").child(device_id).get()

        has_users = False

        if ('privacy' in device_data.val()):
            device_data = device_data.val()
            private = device_data['privacy']
            has_users = True

        add_to_users = []

        if has_users:
            users_ref = db.child('users')
            users = users_ref.get().each()

            for user in users:
                user_data = user.val()
                    
                # Check if 'user_data' exists and has a 'deviceID' key
                if 'user_data' in user_data:
                    if device_id == user_data['user_data']['device_id']:
                        add_to_users.append(user_data['user_data']['id'])

        if image_data:
            # Ensure the 'temp' directory exists
            if not os.path.exists('temp'):
                os.makedirs('temp')
            
            # Save the image temporarily and upload to Firebase Storage
            file_path = os.path.join("temp", filename)
            image_data_bytes = base64.b64decode(image_data.encode('utf-8'))
            with open(file_path, 'wb') as image_file:
                image_file.write(image_data_bytes)
            
            try:
                if not private:
                    storage_path = f"Public/{filename}"
                else:
                    storage_path = f"Private/{filename}"
                storage.child(storage_path).put(file_path)
                image_url = storage.child(storage_path).get_url(None)
            except Exception as e:
                print(f"error {e}")
                return jsonify({'message': 'Error uploading to database'}), 500


            os.remove(file_path) # Delete the temp file

            if len(labels) == 0:
                labels = {}

            user_data = {
                "device_id": device_id,
                "imageURL": image_url,
                "labels": labels,
                "timestamp": time_data,
                "mode": mode_data,
                "processing_location": processing_data
            }

            for uid in add_to_users:
            # Save the data to the database under the user's node
                db.child("users").child(uid).child("images").push(user_data)


        # Check if the user has set keep data to private

        # Search for all users attached to this device id
        # Add the data to those users

        # Store the data in the database (for demonstration purposes, you would use a real database)
        # database[device_id] = {'image': image_data, 'items': items}

        # Return a success message
        return jsonify({'message': 'Data uploaded successfully'}), 200

    except Exception as e:
        print(f"error {e}")

        return jsonify({'message': str(e)}), 500
    

def detect_image(frame):
    global result_queue
    # return (frame, ['person'])
    print("I am detecting image")
    results = model(frame, stream=False)
    items = []
    print("I have ran the model")

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

    print(f"I have detected: {items}")

    result_queue.put((frame, items))


@api_bp.route('/process', methods=['POST'])
def process():
    global result_queue
    # return jsonify("hello"), 500

    print("HELLO")
    try:
        # Get data from the request JSON
        data = request.get_json()

        image_data = data.get('image')
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
        
        # file_path = "./cat_dog.jpg"

        frame = cv2.imread(file_path)


        send_data_thread = threading.Thread(target=detect_image, args=(frame, ))
        send_data_thread.start()
        # frame, labels = detect_image(frame)

        send_data_thread.join()

        frame, labels = result_queue.get()

        # labels = ["Test"]

        print(labels)

        os.remove(file_path) # Delete the temp file

        _, frame_jpeg = cv2.imencode(".jpg", frame)
        image_data_base64 = base64.b64encode(frame_jpeg.tobytes()).decode('utf-8')

        # Convert labels (an array) to a list

        # Prepare a JSON response with image data and labels
        response_data = {
            'image': image_data_base64,
            'labels': labels
        }

        # Return the JSON response
        print("success")
        return jsonify(response_data), 200

    except Exception as e:
        print(f"error {e}")

        return jsonify({'message': str(e)}), 500
    



# from flask import Flask
# from flask_mail import Mail, Message


# # Configuration for sending emails
# mail_server = 'smtp.gmail.com'
# mail_port = 587
# mail_use_tls = True
# mail_username = 'smartvisionhat@gmail.com'
# mail_password = 'smart.123456'

# # Initialize Flask-Mail with the configuration
# mail = Mail()

# def create_api_blueprint(app):
#     # Initialize Flask-Mail with the configuration variables
#     mail.init_app(app, server=mail_server, port=mail_port, use_tls=mail_use_tls,
#                   username=mail_username, password=mail_password)

#     # Pass the app to the blueprint
#     app.register_blueprint(api_bp)

#     return api_bp


# @api_bp.route('/send_email', methods=['POST'])
# def send_email():
#     try:
#         data = request.get_json()
#         device_id = data.get('device_id')

#         # Check if device_id is provided
#         if device_id is None:
#             return jsonify({'message': 'Device ID is required'}), 400
        
#         device_data = db.child("devices").child(device_id).get()

#         has_users = False

#         if ('privacy' in device_data.val()):
#             device_data = device_data.val()
#             has_users = True

#         add_to_users = []

#         if has_users:
#             users_ref = db.child('users')
#             users = users_ref.get().each()

#             for user in users:
#                 user_data = user.val()
                    
#                 # Check if 'user_data' exists and has a 'deviceID' key
#                 if 'user_data' in user_data:
#                     if device_id == user_data['user_data']['device_id']:
#                         add_to_users.append(user_data['user_data']['username'])


#         mail = current_app.extensions['mail']
#         mail_config = current_app.config

#         msg = Message('Subject', sender=mail_username, recipients=add_to_users)

#         msg.body = f"Device id {device_id} wants to alert you. Please check the system log for updates."
#         mail.send(msg)

#         return "success", 200


#     except Exception as e:
#         print(f"error {e}")

#     return jsonify({'message': str(e)}), 500


