import os
from git.repo import Repo
from git.exc import GitCommandError

class GitModule:
    def __init__(self, devassistant_username='Dev Assistant AI', devassistant_email='devassistant@tonet.dev'):
        self.devassistant_username = devassistant_username
        self.devassistant_email = devassistant_email

        self.operations = {
            'init': self.git_init,
            'add': self.git_add,
            'commit': self.git_commit,
            'pull': self.git_pull,
            'checkout': self.git_checkout,
            'push': self.git_push,
            'status': self.git_status,
            'diff': self.git_diff,
            'reset': self.git_reset,
            'log': self.git_log,
            'clone': self.git_clone,
            'branch': self.git_branch,
            'merge': self.git_merge
        }

    def execute(self, operation, arguments=None):
        operation_func = self.operations.get(operation)
        if operation_func:
            if arguments:
                return operation_func(*arguments)
            else:
                return operation_func()
        else:
            return {'error': f'Unknown operation: {operation}. Available operations: {", ".join(self.operations.keys())}'}

    def git_operation(self, operation, directory, *args, **kwargs):
        try:
            repo_path = directory or os.getcwd()
            repo = Repo(repo_path)
            result = getattr(repo.git, operation)(*args, **kwargs)
            return {"message": f"Repo {operation} in {repo_path}", "result": result}
        except GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    def git_init(self, directory):
        return self.git_operation('init', directory)

    def git_add(self, directory):
        return self.git_operation('add', directory, '.')

    def git_commit(self, message, directory, username=None, email=None):
        author = f'{username} <{email}>' if username and email else f'{self.devassistant_username} <{self.devassistant_email}>'
        result = self.git_operation('commit', directory, '-m', message, author=author)
        if "error" in result:
            return {"error": f"Commit failed: {result['error']}"}
        return result

    def git_push(self, remote, branch, directory):
        return self.git_operation('push', directory, remote, branch)

    def git_status(self, directory):
        return self.git_operation('status', directory)

    def git_diff(self, file_path, directory):
        return self.git_operation('diff', directory, file_path)

    def git_reset(self, path):
        return self.git_operation('reset', path)

    def git_log(self, directory):
        return self.git_operation('log', directory)

    def git_pull(self, remote, branch, directory):
        return self.git_operation('pull', directory, remote, branch)

    def git_checkout(self, branch, directory):
        return self.git_operation('checkout', directory, branch)

    def git_clone(self, repository, directory):
        return self.git_operation('clone', directory, repository)

    def git_branch(self, branch, directory):
        return self.git_operation('branch', directory, branch)

    def git_merge(self, branch, directory):
        return self.git_operation('merge', directory, branch)
