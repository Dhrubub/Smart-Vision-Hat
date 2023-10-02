from . import app, db
from flask import render_template, jsonify, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# app = Flask(__name__)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    return render_template('index.html', title='Smart Vision Hat', page_name='Home')

@app.route('/home')
def index2():
    return render_template('home.html', title='Smart Vision Hat', page_name='Home')

@app.route('/settings')
def settings():
    return render_template('settings.html', title='Smart Vision Hat', page_name='Home')

@app.route('/user_manual')
def user_manual():
    return render_template('user_manual.html', title='Smart Vision Hat', page_name='User Manual')

@app.route('/system_log')
def system_log():
    return render_template('system_log.html', title='Smart Vision Hat', page_name='System Log')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html', title='Smart Vision Hat', page_name='About Us')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html', title='Smart Vision Hat', page_name='Contact Us')

@app.route('/ask_page')
def ask_page():
    return render_template('ask.html', title='Smart Vision Hat', page_name='Ask')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.json.get('question')
        user_manual = """User Manual
        1. Insight Snap Mode:
        This mode is designed to quickly identify objects in front of the user.

        a. Click the button.
        b. The camera takes pictures.
        c. The microcontroller and the software analyze the picture.
        d. Objects are detected, and the speaker announces the result.
        Note: This mode is best suited for stationary users who wish to identify objects in their immediate surroundings.

        2. Eyes-On Mode:
        This mode provides continuous visual feedback to the user.

        a. Click the button.
        b. The camera continuously captures pictures.
        c. The microcontroller and the software analyze the pictures.
        d. Objects are detected, and the speaker announces the result.
        Note: This mode is ideal for users on the move. It provides real-time feedback about the user's surroundings.

        3. Vision Assist Mode:
        This mode connects the user with a human assistant for immediate help.

        a. Click the button.
        b. A video call will be established between the vision-impaired individual and their chosen caretaker.
        c. The user can communicate with their caretaker using the built-in microphone to receive guidance.
        Note: This mode is designed for users who require human assistance in unfamiliar or complex environments."""

        instructions = """The above given text is the user manual of our product: Smart Vision Hat.
        And the following text is the questions raised by our user, please answer the questions based on the user manual."""
        
        prompt = f"{instructions}\nQ: {question}\nA:"
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(OPENAI_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        answer = response.json()['choices'][0]['message']['content']
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error: {e}")  # log the error
        return jsonify({"error": "Internal Server Error"}), 500



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/adjust_refresh_rate', methods=['POST'])
def adjust_refresh_rate():
    new_rate = request.json.get('new_rate', 0)
    return jsonify({'status': 'success'})

@app.route('/update_software', methods=['POST'])
def update_software():
    return jsonify({'status': 'software updated'})