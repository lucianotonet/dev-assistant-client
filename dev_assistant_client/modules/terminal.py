import os
import subprocess

TERMINAL_STATE_FILE = os.path.expanduser("~/.dev_assistant_terminal_state")


def execute(operation, args):
    if operation == 'run':
        return run_command(args)
    else:
        return {'error': f'Unknown operation: {operation}'}


def run_command(args):
    try:
        command = args.get('command')
        # Read the current directory from the terminal state file
        current_dir = None
        if os.path.exists(TERMINAL_STATE_FILE):
            with open(TERMINAL_STATE_FILE, 'r') as f:
                current_dir = f.read().strip()
                # Validate the directory path
                if not os.path.isdir(current_dir):
                    current_dir = None
        # Run the command and capture the output
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=current_dir)
        # Check if the command changes the current directory
        if 'cd' in command:
            new_dir = result.stdout.strip()
            if new_dir:
                current_dir = new_dir
                # Save the new current directory to the terminal state file
                with open(TERMINAL_STATE_FILE, 'w') as f:
                    f.write(current_dir)
        return {'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        return {"error": str(e)}# Instructions for the Shell Prompter module

def get_instructions():
    return """
    1. Always validate the command before executing it.
    2. Handle command outputs carefully to avoid errors.
    3. Always close any resources used during command execution.
    4. Use appropriate methods for command execution based on the requirements.
    """