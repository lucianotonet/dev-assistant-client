import os

def execute(operation, args):
    if operation == 'cd':
        return cd(args.get('directory'))
    else:
        return {'error': f'Unknown operation: {operation}'}

def cd(directory):
    try:
        os.chdir(directory)
        return {"message": f"Changed directory to {directory}"}
    except Exception as e:
        return {"error": str(e)}