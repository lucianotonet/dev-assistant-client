
import subprocess

def execute(operation, args):
    if operation == 'run_command':
        return run_command(args.get('request'))
    else:
        return {'error': f'Unknown operation: {operation}'}

def run_command(request):
    try:
        command = request.get('command')
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        return {"error": str(e)}
