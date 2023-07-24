import os
import shutil

def execute(operation, args):
    if operation == 'create':
        return create(args.get('path'), args.get('content'))
    elif operation == 'read':
        return read(args.get('path'))
    elif operation == 'update':
        return update(args.get('path'), args.get('content'))
    elif operation == 'delete':
        return delete(args.get('path'))
    elif operation == 'list':
        return list_dir(args.get('path'))
    elif operation == 'copy':
        return copy(args.get('source'), args.get('destination'))
    elif operation == 'move':
        return move(args.get('source'), args.get('destination'))
    elif operation == 'rename':
        return rename(args.get('source'), args.get('destination'))
    else:
        return {'error': f'Unknown operation: {operation}'}
        
def create(path, content=None):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, 'w', encoding='utf-8') as file:
        if content:
            file.write(content)
    return {"message": f"File created at {path}"}


def read(path):
    if not os.path.exists(path):
        return {"error": f'Path does not exist: {path}'}

    if os.path.isdir(path):
        return list_dir(path)

    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    return {"content": content}


def update(path, content):
    if not os.path.exists(path):
        return {"error": f'File does not exist: {path}'}

    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

    return {"message": f"File updated at {path}"}


def delete(path):
    if not os.path.exists(path):
        return {"error": f'File does not exist: {path}'}

    os.remove(path)
    return {"message": f"File deleted at {path}"}
 
def list_dir(path):
    if not os.path.exists(path):
        return {"error": f'Directory does not exist: {path}'}

    files = os.listdir(path)
    return {"files": files}


def copy(source, destination):
    if not os.path.exists(source):
        return {"error": f'File does not exist: {source}'}

    shutil.copy(source, destination)
    return {"message": f"File copied from {source} to {destination}"}


def move(source, destination):
    if not os.path.exists(source):
        return {"error": f'File does not exist: {source}'}

    shutil.move(source, destination)
    return {"message": f"File moved from {source} to {destination}"}


def rename(source, destination):
    if not os.path.exists(source):
        return {"error": f'File does not exist: {source}'}

    shutil.move(source, destination)
    return {"message": f"File renamed from {source} to {destination}"}
