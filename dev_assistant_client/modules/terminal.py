import subprocess
import logging
from pathlib import Path
from dev_assistant_client.utils import dd

class TerminalModule:
    def __init__(self):
        self.operations = {
            "run": self.run_operation,
            "execute": self.execute_operation,
            "list": self.list_operation,
            "delete": self.delete_operation,
            "copy": self.copy_operation,
            "move": self.move_operation,
        }

    def execute(self, operation, arguments=None):
        # Convert arguments to string if it's a list
        if isinstance(arguments, list):
            arguments = ' '.join(arguments)
        operation_func = self.operations.get(operation)
        if operation_func:
            return operation_func(arguments)
        else:
            raise ValueError(f"Invalid operation: {operation}")

    def run_operation(self, arguments=None):
        # Ensure arguments are a string before validation
        if isinstance(arguments, list):
            arguments = ' '.join(arguments)
        self._validate_arguments(arguments, "run")
        return self._run_external_command(arguments)

    def execute_operation(self, arguments=None):
        self._validate_arguments(arguments, "execute")
        return self._run_external_command(arguments)

    def list_operation(self, arguments=None):
        self._validate_arguments(arguments, "list")
        return self._run_external_command("ls", arguments)

    def delete_operation(self, arguments=None):
        self._validate_arguments(arguments, "delete")
        return self._run_external_command("rm", arguments)

    def copy_operation(self, arguments=None):
        self._validate_arguments(arguments, "copy")
        return self._run_external_command("cp", arguments)

    def move_operation(self, arguments=None):
        self._validate_arguments(arguments, "move")
        return self._run_external_command("mv", arguments)

    def _run_external_command(self, command, arguments=None):
        if not command:
            raise ValueError("No command provided to run.")
        command_list = [command] + (arguments.split() if arguments else [])
        try:
            process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate()
            if process.returncode != 0:
                logging.error(f"Command '{' '.join(command_list)}' failed with error: {error.strip()}")
                raise subprocess.CalledProcessError(process.returncode, command_list, error.strip())
            return output.strip()
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logging.error(f"Failed to run command '{' '.join(command_list)}': {e}")
            raise

    def _validate_arguments(self, arguments, operation):
        if arguments is None:
            raise ValueError(f"No arguments provided for {operation} operation.")
        if not arguments:
            raise ValueError(f"No arguments provided for {operation} operation.")
        if not isinstance(arguments, str):
            raise ValueError(f"Invalid arguments provided for {operation} operation. Expected string, got {type(arguments).__name__}")
            
        
