from . import app, db
from flask import render_template, jsonify, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from dotenv import load_dotenv
import pyrebase
from app.ask_handler import ask_bp
from app.api import api_bp
# from app.sendgrid_email import send_email
import json
import git
import logging
import requests
from collections import defaultdict
import datetime


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app.register_blueprint(ask_bp, url_prefix='/')
app.register_blueprint(api_bp)



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


def reload_pythonanywhere_app():
    username = 'misoto22'
    token = 'f5ed5050a2823a7f39a51b32348a721d374b4d89'
    response = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{username}.pythonanywhere.com/reload/',
        headers={'Authorization': f'Token {token}'}
    )
    return response.status_code == 200


# For Continuous Deployment
@app.route('/git_update', methods=['POST'])
def git_update():
    try:
        repo_path = './Smart-Vision-Hat'
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin

        # Checking out and pulling the 'main' branch
        repo.create_head('main', origin.refs.heads.main).set_tracking_branch(origin.refs.heads.main).checkout()
        origin.pull(branch='main')
        
        logger.info("Successfully pulled from the repo.")
        
        if not reload_pythonanywhere_app():
            logger.error("Failed to reload PythonAnywhere app.")
            return "Failed to reload PythonAnywhere app", 500

        logger.info("Received webhook call and successfully updated and reloaded the app.")
        return '', 200

    except Exception as e:
        logger.error(f"Error in git_update: {str(e)}")
        return str(e), 500


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

            user_data = {
                'id': user_id,
                'username': email,
                "device_id": '',
            }

            # Set or update user data
            db.child("users").child(user_id).child("user_data").set(user_data)


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
            info = auth.get_account_info(user['idToken'])
            user_id = info['users'][0]['localId']
            session['uid'] = user_id
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
        session.pop('uid')
        flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html', title='Smart Vision Hat', page_name='Home')

@app.route('/settings')
def settings():
    if not session.get('username'):
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    user_uid = session.get('uid')
    user_data = db.child("users").child(user_uid).get().val()['user_data']
        
    device_data = db.child("devices").child(user_data['device_id']).get()

    print(device_data.val())

    if 'privacy' in device_data.val():
        # Data exists, retrieve it
        device_data = device_data.val()
        print(device_data)
    else:
        # Data doesn't exist, set it to an empty string
        device_data = {
            "privacy": False,
            "refresh_rate": 20,
        }

    # print(device_data['privacy'])

    return render_template('settings.html', title='Smart Vision Hat', page_name='Home', user_data=user_data, device_data=device_data)

@app.route('/user_manual')
def user_manual():
    return render_template('user_manual.html', title='Smart Vision Hat', page_name='User Manual')


@app.route('/system_log')
def system_log():
    try:
        # Fetch data for the logged-in user from Firebase
        user_uid = session.get('uid')
        user_data = db.child("users").child(user_uid).get().val()

        detected_images = []

        if user_data and "images" in user_data:
            detected_images = list(user_data["images"].values())
        # print(detected_images[-1])
        # Assuming your array is named 'detected_images'
        detected_images = sorted(detected_images, key=lambda x: x['timestamp'], reverse=True)
        # print(detected_images)
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
                    storage_path = f"Public/{uploaded_file.filename}"
                else:
                    storage_path = f"Private/{uploaded_file.filename}"
                storage.child(storage_path).put(file_path)
                image_url = storage.child(storage_path).get_url(None)
            except Exception as e:
                print("Error uploading file:", e)
                flash('Error uploading image to Firebase', 'danger')
                return render_template('upload_img.html')

            os.remove(file_path)

            detected_results = "Example Detected Results"
            
            image_data = {
                "imageURL": image_url,
                "detected_results": detected_results
            }

            user_uid = session.get('uid')
            # Push image data to the 'images' child under the user's UID so a unique image ID is automatically generated
            db.child("users").child(user_uid).child("images").push(image_data)

            flash('Image uploaded and processed!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to upload image', 'danger')
            # Instead of redirecting, render the upload template again
            return render_template('upload_img.html')
    
    # For GET requests, render the upload template
    return render_template('upload_img.html')



from collections import defaultdict

@app.route('/usage_stats')
def usage_stats():
    try:
        user_uid = session.get('uid')
        user_data = db.child("users").child(user_uid).get().val()

        detections_by_object_time = defaultdict(list)
        detections_by_object_count = defaultdict(int)
        mode_counts_time = defaultdict(list)
        hour_counts = defaultdict(int)

        if user_data and "images" in user_data:
            detected_images = list(user_data["images"].values())
            
            for image_data in detected_images:
                labels = image_data.get('labels', {})
                mode = image_data.get('mode', 'Unknown')
                timestamp = image_data.get('timestamp')
                hour = timestamp.split(' ')[1].split(':')[0]

                for object_name, count in labels.items():
                    detections_by_object_time[object_name].append(timestamp)
                    detections_by_object_count[object_name] += count
                
                mode_counts_time[mode].append(timestamp)
                hour_counts[hour] += 1

        sorted_detections = sorted(detections_by_object_count.items(), key=lambda x: x[1], reverse=True)[:10]
        top_10_detections_by_object_time = {k: detections_by_object_time[k] for k, v in sorted_detections}
        sorted_hour_counts = {k: hour_counts[k] for k in sorted(hour_counts)}

        return render_template('usage_stats.html', 
                                title='Smart Vision Hat', 
                                page_name='Usage Stats',
                                detections_by_object_time=top_10_detections_by_object_time, 
                                mode_counts_time=mode_counts_time, 
                                hour_counts=sorted_hour_counts)
    except Exception as e:
        return str(e)





# Ongoing
@app.route('/update_user_data', methods=['POST'])
def update_user_data():
    if not session.get('username'):
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    user_uid = session.get('uid')

    # Assuming you're getting these from a form
    privacy_preference = request.form.get('consent') == '1'  # Converts to boolean
    print(request.form.get('consent'))
    device_id = request.form.get('device_id')
    refresh_rate = int(request.form.get('refresh_rate'))  # Assuming it's a numeric input

    user_data = {
        'id': user_uid,
        'username': session['username'],
        "device_id": device_id,
    }

    if device_id:
        device_data = {
            "privacy": privacy_preference,
            "refresh_rate": refresh_rate,
        }
        db.child("devices").child(device_id).set(device_data)

    # Set or update user data
    db.child("users").child(user_uid).child("user_data").set(user_data)

    flash('User data updated successfully!', 'success')
    return redirect(url_for('settings'))  # Redirect to a settings page or wherever appropriate



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

# @app.route('/send_email', methods=['POST'])
# def send_email():
#     user = request.form.get('user')
#     send_email(user)
#     return redirect(url_for('index'))






@app.route('/adjust_refresh_rate', methods=['POST'])
def adjust_refresh_rate():
    new_rate = request.json.get('new_rate', 0)
    return jsonify({'status': 'success'})

@app.route('/update_software', methods=['POST'])
def update_software():
    return jsonify({'status': 'software updated'})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('components/404.html'), 404

# from flask import Flask
# from flask_mail import Mail, Message


# # Configuration for your email server
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server
# app.config['MAIL_PORT'] = 587  # Use the appropriate port for Gmail
# app.config['MAIL_USE_TLS'] = True  # Gmail requires TLS
# app.config['MAIL_USERNAME'] = 'smartvisionhat@gmail.com'  # Your Gmail email address
# app.config['MAIL_PASSWORD'] = 'smart.123456'  # Your Gmail email password


# # Initialize Flask-Mail
# mail = Mail(app)

# # Create and send an email
# @app.route('/api/send_email', methods=["GET", "POST"])
# def send_email():
#     msg = Message('Hello from Flask-Mail', sender=app.config['MAIL_USERNAME'], recipients=['dhruvjobanputra8@gmail.com'])
#     msg.body = 'This is a test email sent from Flask using Flask-Mail.'
#     mail.send(msg)
#     return 'Email sent successfully.'
