from . import app, db
from flask import render_template, jsonify, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from dotenv import load_dotenv
import pyrebase
from app.ask_handler import ask_bp
from app.api import api_bp  # Import the blueprint from api.py

app.register_blueprint(ask_bp, url_prefix='/')

app.register_blueprint(api_bp)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    return render_template('index.html', title='Smart Vision Hat', page_name='Home')

@app.route('/settings')
def settings():
    return render_template('settings.html', title='Smart Vision Hat', page_name='Home')

@app.route('/user_manual')
def user_manual():
    return render_template('user_manual.html', title='Smart Vision Hat', page_name='User Manual')

@app.route('/system_log')
def system_log():
    return render_template('system_log.html', title='Smart Vision Hat', page_name='System Log')

@app.route('/ask_page')
def ask_page():
    return render_template('ask.html', title='Smart Vision Hat', page_name='Ask')

@app.route('/usage_stats')
def usage_stats():
    return render_template('usage_stats.html', title='Smart Vision Hat', page_name='Usage Stats')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html', title='Smart Vision Hat', page_name='About Us')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html', title='Smart Vision Hat', page_name='Contact Us')






firebaseConfig = {
  'apiKey': "AIzaSyCQAj14X510dN2LreUiVJ-Ox26wqkR_xX8",
  'authDomain': "smart-vision-hat.firebaseapp.com",
  'projectId': "smart-vision-hat",
  'storageBucket': "smart-vision-hat.appspot.com",
  'messagingSenderId': "627181110284",
  'appId': "1:627181110284:web:deb55084063000eb565a29",
  'measurementId': "G-LL0X4KC7S6",
  'databaseURL': ''
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
app.secret_key = "secret"  # Replace this with your own secret key

users = {}  # This is just a simple in-memory data store. In a real-world application, use a database.

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('username')  # Assuming you're using email as a username
        password = request.form.get('password')
        
        try:
            # Register the user with Firebase
            auth.create_user_with_email_and_password(email, password)
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



@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))


@app.route('/adjust_refresh_rate', methods=['POST'])
def adjust_refresh_rate():
    new_rate = request.json.get('new_rate', 0)
    return jsonify({'status': 'success'})

@app.route('/update_software', methods=['POST'])
def update_software():
    return jsonify({'status': 'software updated'})
