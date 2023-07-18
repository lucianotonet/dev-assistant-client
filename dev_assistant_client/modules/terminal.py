import subprocess
import os

def execute(operation, args):
    if operation == 'run':
        return run(args.get('command'))
    else:
        return {'error': f'Unknown operation: {operation}'}

def run(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if process.returncode != 0:
            return {'error': error.decode('utf-8')}
        else:
            return {'output': output.decode('utf-8')}
    except Exception as e:
        return {'error': str(e)}