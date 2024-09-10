# git_operations.py
import git
import os

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

if __name__ == "__main__":
    repo_dir = './dummy_repo'
    commit_and_push_changes(repo_dir)
