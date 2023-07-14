import os
import subprocess

from dev_assistant_client.utils import now

def execute(operation, args):
    if operation == 'run':
        return run(args.get('command'))
    else:
        return {'error': f'Unknown operation: {operation}'}

def run(command):
    try:            
        result = subprocess.run(command, shell=True, capture_output=True, text=True)                        
        return {'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        print(now(), 'Error: ', str(e), sep='\t')
        return {'stdout': '', 'stderr': str(e)}
