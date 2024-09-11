from flask import Flask, request, jsonify
from functions import verify_token, run_pipeline
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the raw payload from the request
    payload = request.get_data()

    # Validate the token in the payload
    if not verify_token(payload):
        return jsonify({'error': 'Invalid token'}), 403

    # Print a success message once the token is validated
    print("Token validated successfully. Webhook event processing...")

    # Get the event type (push, pull_request, etc.)
    event_type = request.headers.get('X-GitHub-Event')

    # Check if the event type is missing
    if not event_type:
        print("No GitHub event type found in headers.")
        return jsonify({'error': 'No event type provided'}), 400

    # Handle different event types
    if event_type == 'push':
        handle_push_event()
    elif event_type == 'pull_request':
        handle_pull_request_event()
    else:
        print(f"Unhandled event type: {event_type}")
        return jsonify({'error': f'Unhandled event type: {event_type}'}), 400

    return jsonify({'status': 'ok'}), 200

# Handle the push event from GitHub
def handle_push_event():
    print("Push event received, generating and testing code...")
    prompt = "Write a Python function that calculates the sum of two numbers. Please only return the code, don't write anything else in your response but just the code."
    run_pipeline(prompt)

# Handle the pull request event
def handle_pull_request_event():
    print("Pull request event received, generating code...")
    prompt = "Write a Python function that calculates the sum of two numbers. Make sure the name of the function should be sum_two_numbers() and there should not be anything else rather than the code in your response."
    run_pipeline(prompt)

if __name__ == '__main__':
    app.run(port=5000)
