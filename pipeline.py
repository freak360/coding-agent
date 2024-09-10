# pipeline.py
import subprocess
from code_generator import generate_code, save_code_to_file
from git_operations import commit_and_push_changes

def run_tests():
    """
    Runs the tests using pytest and returns whether the tests passed or failed.
    """
    result = subprocess.run(['pytest', 'test_generated_code.py'], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0

def run_pipeline(prompt):
    """
    Main pipeline that generates code, tests it, and pushes to Git if tests pass.
    """
    # Step 1: Generate code using OpenAI API
    print("Generating code...")
    code = generate_code(prompt)
    save_code_to_file(code)

    # Step 2: Run tests
    print("Running tests...")
    if run_tests():
        print("All tests passed. Committing and pushing changes.")
        
        # Step 3: Commit and push changes to the repository
        commit_and_push_changes(repo_dir='./dummy_repo', commit_message="Automated code generation and testing")
    else:
        print("Tests failed. Aborting commit.")

if __name__ == "__main__":
    prompt = "Write a Python function that calculates the sum of two numbers."
    run_pipeline(prompt)
