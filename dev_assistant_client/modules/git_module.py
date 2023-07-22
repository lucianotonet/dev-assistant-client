import os
from git import Repo
from git.exc import GitCommandError
from dev_assistant_client.utils import IS_PREMIUM_USER

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
        if IS_PREMIUM_USER:
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
    elif operation == 'log':
        return git_log(args.get('directory'))
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

        # If a username and email are provided, use them for the commit
        if username and email:
            repo.git.commit('-m', message, author=f'{username} <{email}>')
        # Otherwise, use the default username and email for the commit
        else:
            repo.git.commit('-m', message, author=f'{devassistant_username} <{devassistant_email}>')

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

def git_log(directory):
    try:
        repo_path = directory or os.getcwd()
        repo = Repo(repo_path)
        log = repo.git.log()
        return {"message": f"Repo log in {repo_path}", "log": log}
    except GitCommandError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}