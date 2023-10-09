from . import app, db
from flask import render_template, jsonify, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from dotenv import load_dotenv
import pyrebase
from app.ask_handler import ask_bp

app.register_blueprint(ask_bp, url_prefix='/')




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
app.secret_key = "secret"  # Replace this with your own secret key
db = firebase.database()
storage = firebase.storage()

# users = {}  # This is just a simple in-memory data store. In a real-world application, use a database.


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('username')  # Assuming you're using email as a username
        password = request.form.get('password')
        # deviceID = request.form.get('deviceID')  # Assuming you're getting this from the form
        
        try:
            # Register the user with Firebase
            user = auth.create_user_with_email_and_password(email, password)
            info = auth.get_account_info(user['idToken'])
            user_id = info['users'][0]['localId']
            session['uid'] = user_id

            # Store deviceID to database
            # db.child("user_metadata").child(user_id).set({"deviceID": deviceID})

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            error_message = str(e)
            # Check if the error message contains "EMAIL_EXISTS"
            if "EMAIL_EXISTS" in error_message:
                flash('The email address is already in use. Please use a different email or log in.', 'danger')
            else:
                flash('Error during registration. Please try again.', 'danger')
            return redirect(url_for('register'))
    
    return render_template('components/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            user = auth.sign_in_with_email_and_password(username, password)
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        except:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
    
    return render_template('components/login.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html', title='Smart Vision Hat', page_name='Home')

@app.route('/settings')
def settings():
    return render_template('settings.html', title='Smart Vision Hat', page_name='Home')

@app.route('/user_manual')
def user_manual():
    return render_template('user_manual.html', title='Smart Vision Hat', page_name='User Manual')

# Ongoing
@app.route('/system_log')
def system_log():
    try:
        # Fetch the logged data from Firebase
        detected_images_data = db.child("images").get().val()

        detected_images = []
        if detected_images_data:
            for key, value in detected_images_data.items():
                detected_images.append({
                    "image_url": value.get('imageURL'),
                    "detected_object": value.get('detectionResult')
                })

        return render_template('system_log.html', detected_images=detected_images, title='Smart Vision Hat', page_name='System Log')
    except Exception as e:
        # Handle errors as necessary, maybe log them and return a generic error message
        return str(e)


@app.route('/upload_img', methods=['GET', 'POST'])
def upload_img():
    if not session.get('username'):
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        consent_given = request.form.get('consent') == 'yes'
        visibility = consent_given
        if uploaded_file:
            # Ensure the 'temp' directory exists
            if not os.path.exists('temp'):
                os.makedirs('temp')
            
            # Save the image temporarily and upload to Firebase Storage
            file_path = os.path.join("temp", uploaded_file.filename)
            

            uploaded_file.save(file_path)
            try:
                if visibility:
                    storage.child(f"Public/{uploaded_file.filename}").put(file_path)
                else:
                    storage.child(f"Private/{uploaded_file.filename}").put(file_path)
            except Exception as e:
                print("Error uploading file:", e)
                flash('Error uploading image to Firebase', 'danger')
                return render_template('upload_img.html')

            os.remove(file_path) # Delete the temp file

            # For simplicity, assume we save the filename as "image_captured"
            # and detected_results as a constant. Modify this part for actual detection
            detected_results = "Example Detected Results"
            user_data = {
                "image_captured": uploaded_file.filename,
                "detected_results": detected_results
            }

            # Save the data to the database under the user's node
            user_uid = session.get('uid')
            db.child("users").child(user_uid).set(user_data)

            flash('Image uploaded and processed!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to upload image', 'danger')
            # Instead of redirecting, render the upload template again
            return render_template('upload_img.html')
    
    # For GET requests, render the upload template
    return render_template('upload_img.html')



# Ongoing
@app.route('/usage_stats')
def usage_stats():
    try:
        # Fetch the logged data from Firebase
        detected_images_data = db.child("images").get().val()

        # Sample stats - modify this to collect the exact statistics you need
        total_detections = 0
        detections_by_object = {}  # A dictionary to count how many times each object was detected

        if detected_images_data:
            total_detections = len(detected_images_data)
            for key, value in detected_images_data.items():
                detected_object = value.get('detectionResult')
                detections_by_object[detected_object] = detections_by_object.get(detected_object, 0) + 1

        # Convert the dictionary to a format suitable for plotting (if using charts)
        objects_detected = list(detections_by_object.keys())
        objects_counts = list(detections_by_object.values())

        return render_template('usage_stats.html', 
                               total_detections=total_detections, 
                               objects_detected=objects_detected, 
                               objects_counts=objects_counts, 
                               title='Smart Vision Hat', 
                               page_name='Usage Stats')
    except Exception as e:
        # Handle errors as necessary
        return str(e)



@app.route('/ask_page')
def ask_page():
    return render_template('ask.html', title='Smart Vision Hat', page_name='Ask')

# @app.route('/usage_stats')
# def usage_stats():
#     return render_template('usage_stats.html', title='Smart Vision Hat', page_name='Usage Stats')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html', title='Smart Vision Hat', page_name='About Us')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html', title='Smart Vision Hat', page_name='Contact Us')









@app.route('/adjust_refresh_rate', methods=['POST'])
def adjust_refresh_rate():
    new_rate = request.json.get('new_rate', 0)
    return jsonify({'status': 'success'})

@app.route('/update_software', methods=['POST'])
def update_software():
    return jsonify({'status': 'software updated'})