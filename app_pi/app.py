from flask import Flask, request, render_template
import json
import cv2
import base64
# # Initialize your Firebase project configuration
# firebase_config = {
#     "apiKey": "YOUR_API_KEY",
#     "authDomain": "your-app-name.firebaseapp.com",
#     "databaseURL": "https://your-app-name.firebaseio.com",
#     "storageBucket": "your-app-name.appspot.com",
# }

# firebase = pyrebase.initialize_app(firebase_config)

app = Flask(__name__)

# # Access the Firebase Realtime Database
# db = firebase.database()

# # Initialize Firebase Storage
# storage = firebase.storage()

# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     try:
#         # Get the image data from the request
#         image_data = request.get_data()

#         # Upload the image to Firebase Storage
#         image_name = "your_image_name.jpg"  # Replace with a unique image name
#         storage.child("images/" + image_name).put(image_data)

#         return jsonify({"message": "Image uploaded successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Hello"


img = None
items = None

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    global img
    global items
    
    try:
        # Get the image data from the request
        if request.method == 'POST':
            # Get the JSON data from the request
            data = request.get_json()

            # Extract the base64-encoded image data and items from the JSON data
            image_data_base64 = data.get('img', None)
            items_json = data.get('items', '[]')  # Default to empty list if 'items' is not present
            items = json.loads(items_json)


            img_src = 'data:image/jpeg;base64,' + image_data_base64
            print("test")

            # print(image_data)
            img = img_src
        # cv2.imshow('Captured', image_data)

        # Get the items list as JSON data
        # items_json = request.form.get('items')
        # items = json.loads(items_json)

        # Render a template to display the image and items
        # return "get"
        return render_template('display_image.html', image_data=img, items=items)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
