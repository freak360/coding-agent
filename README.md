## Coding Agent: Webhook-Driven Code Generation and Deployment
This project demonstrates how to use a webhook to trigger automated code generation using OpenAI's GPT-4, test it with Pytest, and push the generated code to a separate GitHub repository. The webhook listens for events such as pushes and pull requests and automates the process based on payload data.

This code currently generates a function to calculate the sum of two numbers only, but it can be modified for other purposes.

## **Project Overview**
The Coding Agent project automates the code generation, testing, and deployment process via GitHub Webhooks. Once a webhook event is triggered, the following steps are executed:
1. Generate code using OpenAI's GPT-4 to create a Python function that calculates the sum of two numbers.
2. Test the code with Pytest.
3. Push the code to a separate repository if all tests pass.
This project can be expanded to generate and test other functions as well by modifying the OpenAI prompt.

## **Key Features**
**Webhook Integration:** Responds to GitHub push and pull request events.
**Code Generation:** Automatically generates Python code using GPT-4 based on predefined prompts.
**Automated Testing:** Uses Pytest to validate generated code.
**Git Operations:** Automatically commits and pushes code to a specified GitHub repository.

## Installation and Setup

**1. Clone the Repository**
First, clone the repository locally:

```bash
git clone https://github.com/your-username/coding-agent.git
cd coding-agent
```

**2. Set Up the Virtual Environment**
Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

**3. Install Required Dependencies**
Install the dependencies listed in the requirements.txt:
```bash
pip install -r requirements.txt
```

**4. Configuration**
To configure the project, create a .env file in the root directory with the required environment variables.
.env File
Create a .env file and provide the secret that can be obtained by contacting me:

```bash
# Example Webhook secret for validating the payload token (must match what is set in GitHub)
WEBHOOK_SECRET=c1f4171e7270316e85495432d77554ea95307290
```

**OpenAI API key for generating code**
```bash
OPENAI_API_KEY=your_openai_api_key
```

**GitHub repository URL where the generated code will be pushed**
```bash
NEW_REPO_URL=https://github.com/your-username/generated-code-repo.git
```

**Local path where the repo will be cloned and code will be generated**
```bash
LOCAL_REPO_PATH=D:/projects/generated_repo
```

**Go to your GitHub Repository Settings:**

1. Navigate to Settings > Webhooks.
2. Create a Webhook:
3. Payload URL: Set this to the URL where your Flask app will be listening (e.g., using ngrok).
4. Content Type: Select application/json.
5. Secret: Use the value from your .env file's WEBHOOK_SECRET (e.g., c1f4171e7270316e85485432d77554ea95307290).
**Ngrok Setup (Optional):** If you're testing locally, you can use ngrok to expose your local server to the internet:

```bash
ngrok http 5000
```
Use the generated ngrok URL as the Payload URL in the webhook settings.

**Usage Guide**
Start the Flask Webhook Listener

Start the Flask app to listen for incoming webhook events:

```bash
python webhook_listener.py
```

This will start the webhook listener on http://127.0.0.1:5000. If using ngrok, use the provided public URL.

Triggering the Webhook

When a push or pull request is made to the GitHub repository that has the webhook configured, it will trigger the following pipeline:

**Generate Code:** GPT-4 generates Python code based on a prompt.
**Test Code:** The generated code is automatically tested using Pytest.
**Push Code:**If the tests pass, the code is committed and pushed to the separate repository specified in the .env file.
**Payload Structure**
To trigger the webhook, GitHub sends a JSON payload. Only specific fields are necessary for the webhook to function.

Important Fields:
ref: Branch reference (e.g., refs/heads/main).
repository: Contains repository details like name and URL.
pusher: The individual who triggered the event (name and email).
token: Secret token matching the value stored in .env (WEBHOOK_SECRET).
**Dummy Payload Example:**
Here is a sample dummy payload that could be sent to the webhook:

json
```bash
{
  "ref": "refs/heads/main",
  "before": "abc123",
  "after": "def456",
  "repository": {
    "name": "coding-agent",
    "url": "https://github.com/freak360/coding-agent"
  },
  "pusher": {
    "name": "Aneeb Ajmal",
    "email": "maneebajmal@gmail.com"
  },
  "token": "c1f4171e7270316e84495432d77554ea95307290"
}
```

**This payload includes:**

**ref:** Specifies the branch (refs/heads/main).
**repository:** Contains the repository name and URL.
**pusher:** Information about the person who triggered the event.
**token:** Must match the WEBHOOK_SECRET in your .env file.

**Token Validation:**
The token in the payload must match the secret provided in the .env file for the webhook to process the request.
Functionality:

**Current Functionality:** This project currently generates a Python function to calculate the sum of two numbers. You can modify the prompt in the code to generate other functions.

**Environment Setup:**
Ensure all necessary environment variables are correctly set in the .env file before running the project.

**Dependencies**
All required dependencies are listed in the requirements.txt file. To install them, run:

```bash
pip install -r requirements.txt
```

## **List of Dependencies:**
1. **flask:** For setting up the webhook listener.
2. **openai:** To interact with the OpenAI API for code generation.
3. **pytest:** To run automated tests on the generated code.
4. **python-dotenv:** For loading environment variables from the .env file.
5. **pyngrok:** For exposing the local server to the internet (if needed).
6. **GitPython:** For handling Git operations (commit, push, etc.).

That’s it! You’re now ready to use the Coding Agent project. Feel free to modify or expand its functionality as per your requirements.