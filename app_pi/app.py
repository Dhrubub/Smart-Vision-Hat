import pyrebase
from flask import Flask, request, jsonify, Response

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



@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        # Get the image data from the request
        image_data = request.get_data()

        # Set the content type for the response
        headers = {'Content-Type': 'image/jpeg'}

        # Return the image data as a response
        return Response(image_data, headers=headers)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
