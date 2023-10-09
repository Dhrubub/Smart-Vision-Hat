from flask import Blueprint, jsonify, request
import os
import pyrebase
import json
import uuid
from PIL import Image
import base64


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
        labels_json = data.get('labels', '[]')
        labels = json.loads(labels_json)
        private = False
        filename = str(uuid.uuid4())

        # Check if device_id is provided
        if device_id is None:
            return jsonify({'message': 'Device ID is required'}), 400

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
                print("error upload")
                return jsonify({'message': 'Error uploading to database'}), 500


            os.remove(file_path) # Delete the temp file

            user_data = {
                "device_id": device_id,
                "imageURL": image_url,
                "label": labels
            }

            # Save the data to the database under the user's node
            user_uid = "ya4DaVGaNmdEth3migXHh2zGyCt2"
            db.child("users").child(user_uid).child("images").push(user_data)


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
    

