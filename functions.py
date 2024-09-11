import git
import os
import subprocess
import json
from dotenv import load_dotenv
from openai import OpenAI
import shutil
import re

# Load environment variables from .env file
load_dotenv()

WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI API setup
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Code generation using OpenAI API
def generate_code(prompt):
    """
    Generates code using OpenAI GPT-4 model based on a prompt.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.6,
            messages=[
                {"role": "system", "content": "You are an expert in programming who knows all the computer languages."},
                {"role": "user", "content": prompt},
            ]
        )
        generated_code = completion.choices[0].message.content
        # Use a regular expression to extract the code block
        code_match = re.search(r'```(?:python)?(.*?)```', generated_code, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
        else:
            # If no code block is found, assume the entire response is code
            code = generated_code.strip()

        return code
    except Exception as e:
        print(f"Error while generating code: {str(e)}")
        return e

# Save the generated code to a file
def save_code_to_file(code, filename='generated_code.py'):
    file_path = os.path.join(LOCAL_REPO_PATH, filename)
    
    # Ensure the directory exists
    if not os.path.exists(LOCAL_REPO_PATH):
        os.makedirs(LOCAL_REPO_PATH)
    
    with open(file_path, 'w') as f:
        f.write(code)
    print(f"Code saved to {file_path}")

# Define the repository URL for the separate repo where generated code will be pushed
NEW_REPO_URL = 'https://github.com/freak360/dummy.git'
LOCAL_REPO_PATH = 'D:/projects/generated_repo'  # Directory where the separate repo will be cloned

# Commit and push code changes to the separate repository
def commit_and_push_changes(commit_message="Auto-generated code commit"):
    try:
        # Check if the repository is already cloned and valid
        if not os.path.exists(os.path.join(LOCAL_REPO_PATH, ".git")):
            if os.listdir(LOCAL_REPO_PATH):
                print(f"Directory {LOCAL_REPO_PATH} is not empty but doesn't contain a Git repository. Clearing directory...")
                shutil.rmtree(LOCAL_REPO_PATH)  # Clear the directory if it's not empty and not a Git repository
                os.makedirs(LOCAL_REPO_PATH)  # Recreate the directory
            print(f"Cloning repository from {NEW_REPO_URL} to {LOCAL_REPO_PATH}...")
            git.Repo.clone_from(NEW_REPO_URL, LOCAL_REPO_PATH)
        else:
            print(f"Repository already exists at {LOCAL_REPO_PATH}. Pulling latest changes...")
            repo = git.Repo(LOCAL_REPO_PATH)
            origin = repo.remote(name='origin')
            origin.pull()

        # Load the repository from the local path
        repo = git.Repo(LOCAL_REPO_PATH)

        # Stage all changes (we assume generated code is saved to this repo)
        repo.git.add(all=True)

        # Commit changes
        repo.index.commit(commit_message)

        # Push to the remote repository (assuming 'origin' is the remote)
        origin = repo.remote(name='origin')
        origin.push()
        print("Changes pushed to the separate repository.")
    except Exception as e:
        print(f"Error while pushing to the separate Git repository: {str(e)}")

# Run tests using Pytest
def run_tests():
    result = subprocess.run(['pytest', 'test_generated_code.py'], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0

# Simplified token verification, without signature validation
def verify_token(data):
    try:
        # Parse the payload and check if the token matches the expected token
        payload = json.loads(data)
        print(f"Token in payload: {payload.get('token')}")
        print(f"Expected token: {WEBHOOK_SECRET_TOKEN}")
        
        # Validate the token in the payload
        if 'token' not in payload or payload['token'] != WEBHOOK_SECRET_TOKEN:
            print("Token mismatch or token not provided in the payload.")
            return False
    except Exception as e:
        print(f"Error processing the payload: {str(e)}")
        return False

    # If the token matches, proceed with the request
    print("Token verified successfully.")
    return True

# Main pipeline to handle code generation, testing, and pushing
def run_pipeline(prompt):
    print("Generating code...")
    code = generate_code(prompt)
    save_code_to_file(code)

    print("Running tests...")
    if run_tests():
        print("All tests passed. Committing and pushing changes to separate repository.")
        commit_and_push_changes(commit_message="Automated code generation and testing")
    else:
        print("Tests failed. Aborting commit.")
