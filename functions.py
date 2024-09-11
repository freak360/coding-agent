import git
import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI
import hmac
import hashlib

# Load environment variables from .env file
load_dotenv()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
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
        return generated_code.strip()
    except Exception as e:
        print(f"Error while generating code: {str(e)}")
        return e

# Save the generated code to a file
def save_code_to_file(code, filename='generated_code.py'):
    with open(filename, 'w') as f:
        f.write(code)
    print(f"Code saved to {filename}")

# Commit and push code changes to the repository
def commit_and_push_changes(repo_dir, commit_message="Auto-generated code commit"):
    try:
        repo = git.Repo(repo_dir)
        repo.git.add(all=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
        print("Changes pushed to remote repository.")
    except Exception as e:
        print(f"Error while pushing to Git: {str(e)}")

# Run tests using Pytest
def run_tests():
    result = subprocess.run(['pytest', 'test_generated_code.py'], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0

# Verify the webhook signature from GitHub
def verify_signature(data, signature):
    if signature is None:
        return False
    mac = hmac.new(bytes(WEBHOOK_SECRET, 'utf-8'), msg=data, digestmod=hashlib.sha256)
    return hmac.compare_digest('sha256=' + mac.hexdigest(), signature)

# Main pipeline to handle code generation, testing, and pushing
def run_pipeline(prompt, repo_dir='./dummy_repo'):
    print("Generating code...")
    code = generate_code(prompt)
    save_code_to_file(code)

    print("Running tests...")
    if run_tests():
        print("All tests passed. Committing and pushing changes.")
        commit_and_push_changes(repo_dir=repo_dir, commit_message="Automated code generation and testing")
    else:
        print("Tests failed. Aborting commit.")
