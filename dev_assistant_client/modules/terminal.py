import os
import subprocess
import logging
import shlex
from pathlib import Path
from dev_assistant_client.utils import TERMINAL_CWD_FILE
import platform
import glob

class TerminalModule:
    def __init__(self):
        self.cwd_file = TERMINAL_CWD_FILE
        self.current_dir = self._load_cwd()  # Load or default to current working directory
        logging.basicConfig(level=logging.INFO)  # Configure logging

    def _load_cwd(self):
        """Load the saved current working directory, or default to the system's CWD."""
        try:
            if self.cwd_file.exists():
                with open(self.cwd_file, 'r') as file:
                    saved_dir = file.read().strip()
                    if Path(saved_dir).exists():
                        return saved_dir
        except Exception as e:
            logging.error(f"Error loading saved CWD: {e}")
        return os.getcwd()

    def _save_cwd(self):
        """Save the current working directory."""
        try:
            with open(self.cwd_file, 'w') as file:
                file.write(self.current_dir)
        except Exception as e:
            logging.error(f"Error saving CWD: {e}")

    def change_directory(self, path):
        """Change the current working directory."""
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
            self._save_cwd()
            logging.info(f"Changed directory to {self.current_dir}")
            return f"Changed directory to {self.current_dir}"
        except FileNotFoundError:
            logging.error(f"Directory '{path}' not found.")
            return f"Error: Directory '{path}' not found."
        except OSError as e:
            logging.error(f"OS error: {e}")
            return f"Error: {e}"

    def execute(self, operation, arguments=None):
        """Execute a given operation with optional arguments."""
        if operation == 'cd':
            return self._execute_cd(arguments)
        return self.run_command(operation, arguments)

    def _execute_cd(self, arguments):
        """Execute 'cd' operation."""
        if arguments:
            full_path = self._build_full_path(arguments)
            return self.change_directory(full_path)
        else:
            logging.error("No path provided for 'cd' command.")
            return "Error: No path provided for 'cd' command."

    def _build_full_path(self, path):
        """Build a full path from a given input, resolving home directory references."""
        try:
            if path.startswith('~'):
                return str(Path.home() / path.strip('~'))
            elif path.lower() == 'desktop':
                return self._get_desktop_path()
            else:
                return str(Path(self.current_dir) / path)
        except Exception as e:
            logging.error(f"Error building full_path: {e}")
            return str(Path(self.current_dir) / path)  # Fallback to the current directory

    def _get_desktop_path(self):
        """Get the path to the desktop."""
        if platform.system() == 'Windows':
            return str(Path.home() / 'Desktop')
        elif platform.system() == 'Darwin':
            return str(Path.home() / 'Desktop')
        else:
            return str(Path.home() / 'Desktop')

    def run_command(self, command, arguments=None):
        """Run a given command with optional arguments."""
        if command == 'ls':
            return self._run_ls()
        return self._run_other_command(command, arguments)

    def _run_ls(self):
        """Run 'ls' command."""
        try:
            files = glob.glob(self.current_dir + '/*')
            return '\n'.join(files)
        except Exception as e:
            logging.error(f"Failed to list files in directory '{self.current_dir}': {e}")
            return f"Error: {e}"

    def _run_other_command(self, command, arguments):
        """Run other command."""
        if not command:
            logging.error("No command provided to run.")
            return "Error: No command provided to run."

        command_list = [command] + ([shlex.quote(arg) for arg in arguments.split()] if arguments else [])

        try:
            process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', cwd=self.current_dir)
            output, error = process.communicate()

            if process.returncode != 0:
                error_message = error.strip() if error else 'Unknown error'
                logging.error(f"Command '{' '.join(command_list)}' failed with error: {error_message}")
                return f"Error: {error_message}"

            return output.strip() if output and output.strip() else "Success: Command executed without output."
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logging.error(f"Failed to run command '{' '.join(command_list)}': {e}")
            return f"Error: {e}"
