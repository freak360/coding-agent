# webhook_listener.py
from flask import Flask, request, jsonify
import subprocess
import hmac
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import webhook secret
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = Flask(__name__)

def verify_signature(data, signature):
    mac = hmac.new(bytes(WEBHOOK_SECRET, 'utf-8'), msg=data, digestmod=hashlib.sha256)
    return hmac.compare_digest('sha256=' + mac.hexdigest(), signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature-256')

    print(f"Payload: {payload}")  # Debugging payload
    print(f"Signature: {signature}")  # Debugging signature

    # Verify webhook signature
    if not verify_signature(payload, signature):
        return jsonify({'error': 'Invalid or missing signature'}), 403

    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        handle_push_event()
    elif event_type == 'pull_request':
        handle_pull_request_event()

    return jsonify({'status': 'ok'}), 200

def handle_push_event():
    print("Push event received, generating and testing code...")
    # Call the code generation and testing pipeline
    subprocess.run(['python', 'pipeline.py'])

def handle_pull_request_event():
    print("Pull request event received, generating code...")
    # Call the code generation without testing, or test if needed
    subprocess.run(['python', 'pipeline.py'])

if __name__ == '__main__':
    app.run(port=5000)
