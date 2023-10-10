from flask import Blueprint, jsonify, request
import requests
import os
from dotenv import load_dotenv
from requests.exceptions import RequestException, Timeout, TooManyRedirects, HTTPError

# product_info path
product_info_dir = './product_info/'

# Activate the ask blueprint
ask_bp = Blueprint('ask_bp', __name__)

# Load environment variables - OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

def read_file(filepath):
            with open(filepath, 'r') as f:
                return f.read()

@ask_bp.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.json.get('question')

        product_info = read_file(product_info_dir + 'product_info.txt')
        user_manual = read_file(product_info_dir + 'user_manual.txt')
        instructions = read_file(product_info_dir + 'instructions.txt')
        
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

    except Timeout:
        print("Request to OpenAI timed out.")
        return jsonify({"error": "Request timed out"}), 504

    except TooManyRedirects:
        print("Request to OpenAI had too many redirects.")
        return jsonify({"error": "Too many redirects"}), 508

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g. 404 or 500
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), 500

    except RequestException as req_err:
        print(f"Request to OpenAI failed: {req_err}")
        return jsonify({"error": "API request failed"}), 500

    except Exception as e:
        print(f"Unexpected error: {e}")  # log the error
        return jsonify({"error": "Internal Server Error"}), 500