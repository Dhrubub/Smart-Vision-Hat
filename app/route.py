from . import app, db
from flask import render_template, jsonify, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from dotenv import load_dotenv
from app.ask_handler import ask_bp

app.register_blueprint(ask_bp, url_prefix='/')



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