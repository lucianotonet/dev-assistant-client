import subprocess
import os
import shutil
import logging
from pathlib import Path
from dev_assistant_client.utils import dd

class TerminalModule:
    def __init__(self):
        self.operations = {
            "list": self.list_dir,
            "cd": self.change_directory,
            "mkdir": self.create_directory,
            "rmdir": self.remove_directory,
            "cp": self.copy,
            "mv": self.move,
            "rm": self.remove,
            "rename": self.rename,
        }

    def execute(self, operation, arguments=None):
        operation_func = self.operations.get(operation)
        if operation_func:
            # Se 'arguments' for None ou uma lista vazia, chame a função sem argumentos.
            if not arguments:
                return operation_func()
            # Se 'arguments' for uma lista, desempacote os argumentos.
            elif isinstance(arguments, list):
                return operation_func(*arguments)
            # Se 'arguments' for um único argumento que não seja uma lista, passe-o diretamente.
            else:
                return operation_func(arguments)
        else:
            # Se a operação não estiver no dicionário 'operations', execute o comando externo.
            return self.run(operation, arguments)

    def run(self, command, arguments=None):
        response = None
        try:
            # Garante que o comando seja uma lista
            if isinstance(command, str):
                command = command.split()
            # Se 'arguments' for None, usa uma lista vazia
            full_command = command + (arguments or [])
            process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if process.returncode != 0:
                logging.error(error.decode('utf-8'))
            else:
                response = output.decode('utf-8').strip()
        except subprocess.SubprocessError as e:
            logging.error(str(e))
        except FileNotFoundError as e:
            logging.error(str(e))
            response = str(e)
        return response

    def list_dir(self, directory='.'):
        try:
            return '\n'.join([str(file) for file in Path(directory).iterdir()])
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
            os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
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
