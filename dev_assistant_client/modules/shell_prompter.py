
import subprocess

def execute(operation, args):
    if operation == 'run':
        return run_command(args)
    else:
        return {'error': f'Unknown operation: {operation}'}

def run_command(args):
    try:
        command = args.get('command')
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        return {"error": str(e)}
