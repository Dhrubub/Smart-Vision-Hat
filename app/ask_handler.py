from flask import Blueprint, jsonify, request
import requests
import os
from dotenv import load_dotenv


ask_bp = Blueprint('ask_bp', __name__)

def read_file(filepath):
            with open(filepath, 'r') as f:
                return f.read()

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# app = Flask(__name__)

@ask_bp.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.json.get('question')

        product_info = read_file('product_info/product_info.txt')
        user_manual = read_file('product_info/user_manual.txt')
        instructions = read_file('product_info/instructions.txt')
        
        prompt = f"{product_info}\n{user_manual}\n{instructions}\nQ: {question}\nA:"
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