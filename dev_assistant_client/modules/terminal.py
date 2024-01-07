import subprocess
import logging
from pathlib import Path
from dev_assistant_client.utils import dd
import shlex
import subprocess
import logging

class TerminalModule:
    def __init__(self):
        pass
    
    def execute(self, operation, arguments=None):
        # Convert arguments to string if it's a list
        if isinstance(arguments, list):
            arguments = ' '.join(arguments)
        
        return self._run_external_command(operation, arguments)

    def _run_external_command(self, command, arguments=None):
        if not command:
            return "Error: No command provided to run."

        # Garante que os argumentos sejam strings e os escapar de forma segura
        command_list = [command] + ([shlex.quote(str(arg)) for arg in arguments.split()] if arguments else [])
        
        try:
            process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
            output, error = process.communicate()

            if process.returncode != 0:
                error_message = error.strip() if error else 'Unknown error'
                logging.error(f"Command '{' '.join(command_list)}' failed with error: {error_message}")
                return f"Error: {error_message}"

            return output.strip() if output and output.strip() else "Success: Command executed without output."

        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logging.error(f"Failed to run command '{' '.join(command_list)}': {e}")
            return f"Error: {e}"
