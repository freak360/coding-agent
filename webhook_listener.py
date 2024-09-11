# webhook_listener.py
from flask import Flask, request, jsonify
from functions import verify_signature, run_pipeline
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    signature = request.headers.get('X-Hub-Signature-256')

    # Debugging output
    print(f"Payload: {payload}")
    print(f"Signature: {signature}")

    # Verify the webhook signature
    if not verify_signature(payload, signature):
        return jsonify({'error': 'Invalid or missing signature'}), 403

    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        handle_push_event()
    elif event_type == 'pull_request':
        handle_pull_request_event()

    return jsonify({'status': 'ok'}), 200

# Handle the push event from GitHub
def handle_push_event():
    print("Push event received, generating and testing code...")
    prompt = "Write a Python function that calculates the sum of two numbers."
    run_pipeline(prompt)

# Handle the pull request event
def handle_pull_request_event():
    print("Pull request event received, generating code...")
    prompt = "Write a Python function that calculates the sum of two numbers."
    run_pipeline(prompt)

if __name__ == '__main__':
    app.run(port=5000)
