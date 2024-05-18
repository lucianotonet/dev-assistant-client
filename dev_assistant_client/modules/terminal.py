import json
import os
import subprocess
import logging
import shlex
from pathlib import Path
from ..utils import StateManager
import platform
import glob
import json

class TerminalModule:
    def __init__(self, instruction):
        self.client_id = instruction.get("client_id")
        self.feedback = instruction.get("feedback")
        self.module = instruction.get("module")
        self.operation = instruction.get("operation")
        self.arguments = instruction.get("arguments")
        
        self.state_manager = StateManager()  # Instancia StateManager
        self.state = self.state_manager.get_state()  # Carrega o estado
        
        self.current_dir = self.state.get("cwd", os.getcwd())  # Carrega o diretório atual
        self.operations = {
            "run": self.run_command,
            "cd": self.change_directory,  # Mapeia a operação 'cd' para o método change_directory
            "cwd": self.get_current_directory,  # Mapeia a operação 'cwd' para o método get_current_directory
            "execute": self.run_command,  # Mapeia a operação 'execute' para o método run_command 
            "api_spec": self.get_api_spec
        }
        
    def get_api_spec(self, *args):
        return {
            "module": "Terminal",
            "operations": {
                "run": {"summary": "Run a command", "parameters": [{"name": "command_with_args", "in": "query", "type": "string", "description": "The command to run with its arguments"}]},
                "cd": {"summary": "Change the current working directory", "parameters": [{"name": "path_list", "in": "query", "type": "string", "description": "The path or paths to change the directory to, separated by a space"}]},
                "cwd": {"summary": "Get the current working directory", "parameters": [], "responses": {"200": {"content": {"application/json": {"schema": {"type": "object", "properties": {"cwd": {"type": "string"}}}}}}}},
                "execute": {"summary": "Run a command", "parameters": [{"name": "command_with_args", "in": "query", "type": "string", "description": "The command to run with its arguments"}]}
            }
        }
    
    def execute(self):
        operation_func = self.operations.get(self.operation, self.unknown_operation)
        if self.arguments is None:
            self.arguments = []
        try:
            execute_response = operation_func(self.arguments)
            return json.dumps(execute_response)
        except TypeError as e:
            logging.error(f"Type error during command execution: {e}")
            return json.dumps({'error': f'Error: Type error - {str(e)}'}, ensure_ascii=False)
        except FileNotFoundError as e:
            return json.dumps({'error': str(e)}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'error': f'Error in {self.operation}: {str(e)}'}, ensure_ascii=False)

    def unknown_operation(self, args):
        valid_operations = list(self.operations.keys())
        return json.dumps({'error': f'Unknown operation: {self.operation}', 'valid_operations': valid_operations})

    def _load_context(self):
        """Load the saved terminal context."""
        base_context = {
            "cwd": os.getcwd(),
            "system": platform.system(),
            "user": os.getlogin(),
        }
        context = self.state_manager.get_state()  # Get the state from the StateManager
        if not context:
            context = base_context
        return context

    def _save_context(self, context):
        """Save the terminal context."""
        context["os"] = platform.system()
        context["user"] = os.getlogin()
        
        self.state_manager.set_state(context)  # Save the context using the StateManager

    def change_directory(self, path_list):
        """Change the current working directory."""
        path = path_list[0] if path_list else None
        try:
            os.chdir(path)
            self.state = self._load_context()
            self.state["cwd"] = os.getcwd()  # Update the directory in the state
            self._save_context(self.state)  # Save the updated state to the file
            logging.info(f"Changed directory to {self.state['cwd']}")
            return f"Changed directory to {self.state['cwd']}"
        except FileNotFoundError:
            logging.error(f"Directory '{path}' not found.")
            return f"Error: Directory '{path}' not found."
        except OSError as e:
            logging.error(f"OS error: {e}")
            return f"Error: {e}"

    def get_current_directory(self, args):
        return self.state["cwd"]
    
    def run_command(self, command_with_args):
        """Run a given command with optional arguments."""
        if not command_with_args:
            logging.error("No command provided to run.")
            return "Error: No command provided to run."

        command, *arguments = command_with_args  # Separa o comando dos argumentos

        if command == 'ls':
            return self._run_ls()
        else:
            return self._run_other_command(command, arguments)

    def _run_ls(self):
        """Run 'ls' command."""
        try:
            files = glob.glob(self.state['cwd'] + '/*')
            return '\n'.join(files)
        except Exception as e:
            logging.error(f"Failed to list files in directory '{self.state['cwd']}': {e}")
            return f"Error: {e}"

    def _run_other_command(self, command, arguments):
        """Run other command, with special handling for Windows 'dir' command."""
        if not command:
            logging.error("No command provided to run.")
            return "Error: No command provided to run."

        # Normaliza o comando para o ambiente correto
        command_list = self._normalize_command(command, arguments)

        try:
            process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', cwd=self.state['cwd'], shell=True)
            output, error = process.communicate()

            if process.returncode != 0:
                error_message = error.strip() if error else 'Unknown error'
                logging.error(f"Command '{' '.join(command_list)}' failed with error: {error_message}")
                return f"Error: {error_message}"

            return output.strip() if output and output.strip() else "Success: Command executed without output."
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logging.error(f"Failed to run command '{' '.join(command_list)}': {e}")
            return f"Error: {e}"

    def _normalize_command(self, command, arguments):
        """Adjust the command based on the operating system."""
        # Escapes arguments to avoid command injection
        arguments = [shlex.quote(arg) for arg in arguments] if arguments else []
        if platform.system() == 'Windows':
            # List of commands that need special handling in Windows
            windows_commands = ['dir', 'copy', 'del', 'move', 'rename']
            if command.lower() in windows_commands:
                return ['cmd', '/c', command] + arguments
            else:
                # All other specific Windows commands are handled here
                return ['cmd', '/c', command] + arguments
        elif platform.system() == 'Linux':
            # List of commands that need special handling in Linux
            linux_commands = ['ls', 'cp', 'rm', 'mv', 'rename']
            if command.lower() in linux_commands:
                return ['bash', '-c', command] + arguments
            else:
                # All other specific Linux commands are handled here
                return ['bash', '-c', command] + arguments
        return [command] + arguments