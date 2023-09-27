import csv
from flask import Flask, jsonify, render_template, request, send_from_directory


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/analyse')
def analyse():
    return render_template('analyse.html')


if __name__ == '__main__':
    app.run(debug=True)

