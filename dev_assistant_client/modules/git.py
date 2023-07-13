
import os
from git import Repo, GitCommandError

def execute(operation, args):
    if operation == 'init':
        return git_init(args.get('directory'))
    elif operation == 'add':
        return git_add(args.get('directory'))
    elif operation == 'commit':
        return git_commit(args.get('message'), args.get('directory'))
    elif operation == 'push':
        return git_push(args.get('remote'), args.get('branch'), args.get('directory'))
    elif operation == 'status':
        return git_status(args.get('directory'))
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

def git_commit(message, directory):
    try:
        repo_path = directory or os.getcwd()
        repo = Repo(repo_path)
        repo.git.commit('-m', message)
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
# Instructions for the Version Control module

def get_instructions():
    return """
    1. Always validate the repository path before performing operations.
    2. Handle git commands and their outputs carefully to avoid errors.
    3. Always close any resources used during command execution.
    4. Use appropriate git commands based on the requirements.
    """