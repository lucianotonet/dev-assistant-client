import os
import subprocess
from git import Repo, GitCommandError

# Add a global variable for premium users
is_premium_user = False

# Add the DevAssistant's username and email
devassistant_username = 'Dev Assistant AI'
devassistant_email = 'devassistant@tonet.dev'

def execute(operation, args):
    if operation == 'init':
        return git_init(args.get('directory'))
    elif operation == 'add':
        return git_add(args.get('directory'))
    elif operation == 'commit':
        # For premium users, use their username and email for commits
        if is_premium_user:
            return git_commit(args.get('message'), args.get('directory'), args.get('username'), args.get('email'))
        # For non-premium users, use the DevAssistant's username and email for commits
        else:
            return git_commit(args.get('message'), args.get('directory'), devassistant_username, devassistant_email)
    elif operation == 'push':
        return git_push(args.get('remote'), args.get('branch'), args.get('directory'))
    elif operation == 'status':
        return git_status(args.get('directory'))
    elif operation == 'diff':
        return git_diff(args.get('file_path'), args.get('directory'))
    else:
        return {'error': f'Unknown operation: {operation}'}

def git_init(directory):
    try:
        repo_path = directory or os.getcwd()
        Repo.init(repo_path)
        return {"message": f"Repo init in {repo_path}"}
    except GitCommandError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def git_add(directory):
    try:
        repo_path = directory or os.getcwd()
        repo = Repo(repo_path)
        repo.git.add('.')
        return {"message": f"Repo add in {repo_path}"}
    except GitCommandError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def git_commit(message, directory, username=None, email=None):
    try:
        repo_path = directory or os.getcwd()
        repo = Repo(repo_path)

        # Save the current user.name and user.email
        current_username = repo.config_reader().get_value("user", "name")
        current_email = repo.config_reader().get_value("user", "email")

        # If a username and email are provided, set them
        if username and email:
            repo.config_writer().set_value("user", "name", username)
            repo.config_writer().set_value("user", "email", email)

        # Commit the changes
        repo.git.commit('-m', message)

        # Reset the user.name and user.email to their original values
        repo.config_writer().set_value("user", "name", current_username)
        repo.config_writer().set_value("user", "email", current_email)

        return {"message": f"Repo commit in {repo_path}"}
    except GitCommandError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def git_push(remote, branch, directory):
    try:
        repo_path = directory or os.getcwd()
        repo = Repo(repo_path)
        repo.git.push(remote, branch)
        return {"message": f"Repo push in {repo_path}"}
    except GitCommandError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def git_status(directory):
    try:
        repo_path = directory or os.getcwd()
        repo = Repo(repo_path)
        return {"message": f"Repo status in {repo_path}", "status": repo.git.status()}
    except GitCommandError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def git_diff(file_path, directory):
    try:
        repo_path = directory or os.getcwd()
        repo = Repo(repo_path)
        diff = repo.git.diff(file_path)
        return {"message": f"Repo diff in {repo_path}", "diff": diff}
    except GitCommandError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}