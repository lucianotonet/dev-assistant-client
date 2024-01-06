import json
import logging
import subprocess

class GitModule:
    def __init__(self, working_directory=None):
        self.module = "git"
        self.working_directory = working_directory
        self.operations = {
            "clone": self.clone,
            "status": self.status,
            "checkout": self.checkout,
            "add": self.add,
            "commit": self.commit,
            "push": self.push,
            "pull": self.pull,
            "fetch": self.fetch,
            "merge": self.merge,
            "rebase": self.rebase,
            "reset": self.reset,
            "log": self.log
        }
        logging.basicConfig(level=logging.INFO)
        
    def execute(self, operation, arguments=None):
        if operation in self.operations:
            try:
                result = self.operations[operation](arguments if arguments else [])
                logging.info(f"{operation} executed successfully")
                return result
            except subprocess.CalledProcessError as e:
                logging.error(f"Command failed: {e.cmd}")
                return e.output.decode("utf-8")
            except Exception as e:
                logging.exception("Unexpected error")
                return str(e)
        else:
            return json.dumps({"error": f"Unsupported operation: {operation}"})

    def clone(self, arguments):
        if not arguments or len(arguments) < 1:
            raise ValueError("You must specify a repository to clone.")
        return self._run_git_command(["clone"] + arguments)

    def _run_git_command(self, command):
        full_command = ["git"] + command
        logging.info(f"Running command: {' '.join(full_command)}")
        print(f"Running command: {' '.join(full_command)}")
        response = subprocess.check_output(
            full_command, cwd=self.working_directory, stderr=subprocess.STDOUT
        )
        return json.dumps(response.decode("utf-8"))

    def checkout(self, arguments):
        if not arguments:
            raise ValueError("You must specify a branch or commit to checkout.")
        return self._run_git_command(["checkout"] + arguments)

    def add(self, arguments):
        if not arguments:
            raise ValueError("You must specify a file or pattern to add.")
        return self._run_git_command(["add"] + arguments)

    def commit(self, arguments):
        if not arguments or "--message" not in arguments:
            raise ValueError("You must specify a commit message using '--message'.")
        return self._run_git_command(["commit"] + arguments)

    def push(self, arguments):
        return self._run_git_command(["push"] + arguments)

    def pull(self, arguments):
        return self._run_git_command(["pull"] + arguments)

    def fetch(self, arguments):
        return self._run_git_command(["fetch"] + arguments)

    def merge(self, arguments):
        if not arguments:
            raise ValueError("You must specify a branch to merge.")
        return self._run_git_command(["merge"] + arguments)

    def rebase(self, arguments):
        if not arguments:
            raise ValueError("You must specify a branch to rebase onto.")
        return self._run_git_command(["rebase"] + arguments)

    def reset(self, arguments):
        return self._run_git_command(["reset"] + arguments)

    def log(self, arguments):
        return self._run_git_command(["log"] + arguments)

    def status(self, arguments):
        return self._run_git_command(["status"] + arguments)


