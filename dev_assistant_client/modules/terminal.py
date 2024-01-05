import subprocess
import os
import shutil
import logging
from pathlib import Path

class TerminalModule:
    def __init__(self):
        self.operations = {
            "list": self.list_dir,
            "change_directory": self.change_directory,
            "create_directory": self.create_directory,
            "remove_directory": self.remove_directory,
            "copy": self.copy,
            "move": self.move,
            "remove": self.remove,
            "rename": self.rename,
        }

    def execute(self, operation, arguments=None):
        operation_func = self.operations.get(operation)
        if operation_func:
            return operation_func(arguments)
        else:
            # If operation is not in the predefined list, try to execute it as a shell command
            try:
                if arguments:
                    return self.run(operation, arguments)
                else:
                    return self.run(operation)
            except Exception as e:
                logging.error(f'Failed to execute operation: {operation}. Error: {str(e)}')
                return None

    def run(self, command, arguments=None):
        try:
            process = subprocess.Popen([command] + arguments if arguments else [command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if process.returncode != 0:
                logging.error(error.decode('utf-8'))
                return None
            return output.decode('utf-8')
        except subprocess.SubprocessError as e:
            logging.error(str(e))
            return None

    def list_dir(self, directory=None):
        try:
            path = Path(directory if directory else '.')
            return '\n'.join([str(file) for file in path.iterdir()])
        except OSError as e:
            logging.error(str(e))
            return None

    def change_directory(self, directory):
        try:
            os.chdir(directory)
            return f'Changed directory to {directory}'
        except OSError as e:
            logging.error(str(e))
            return None

    def create_directory(self, directory):
        try:
            os.makedirs(directory)
            return f'Created directory {directory}'
        except OSError as e:
            logging.error(str(e))
            return None

    def remove_directory(self, directory):
        try:
            shutil.rmtree(directory)
            return f'Removed directory {directory}'
        except OSError as e:
            logging.error(str(e))
            return None

    def copy(self, source, destination):
        try:
            shutil.copy2(source, destination)
            return f'Copied {source} to {destination}'
        except OSError as e:
            logging.error(str(e))
            return None

    def move(self, source, destination):
        try:
            shutil.move(source, destination)
            return f'Moved {source} to {destination}'
        except OSError as e:
            logging.error(str(e))
            return None

    def remove(self, path):
        try:
            os.remove(path)
            return f'Removed {path}'
        except OSError as e:
            logging.error(str(e))
            return None

    def rename(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            return f'Renamed {old_name} to {new_name}'
        except OSError as e:
            logging.error(str(e))
            return None
