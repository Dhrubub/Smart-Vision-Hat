from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os

OPENAI_API_KEY = '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'
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    return render_template('index.html', title='Smart Vision Hat')

@app.route('/home')
def index2():
    return render_template('home.html', title='Smart Vision Hat')

@app.route('/settings')
def settings():
    return render_template('settings.html', title='Smart Vision Hat')

@app.route('/user_manual')
def user_manual():
    return render_template('user_manual.html', title='Smart Vision Hat')

@app.route('/system_log')
def system_log():
    return render_template('system_log.html', title='Smart Vision Hat')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html', title='Smart Vision Hat')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html', title='Smart Vision Hat')

@app.route('/ask_page')
def ask_page():
    return render_template('ask.html', title='Smart Vision Hat')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    data = {
        "model": "gpt-4.0-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(OPENAI_ENDPOINT, headers=headers, json=data)
    if response.status_code != 200:
        return jsonify({"error": "Failed to get response from OpenAI", "details": response.json()})
    response_data = response.json()
    
    answer = response_data['choices'][0]['message']['content']
    return jsonify({"answer": answer})


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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)