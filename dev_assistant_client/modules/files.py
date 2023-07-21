import logging
import os
import shutil
class FileOperationException(Exception):
    pass

def execute(operation, args):
    operations = {
        'create': create,
        'read': read,
        'update': update,
        'delete': delete,
        'list': list_dir,
        'copy': copy,
        'move': move,
        'rename': rename
    }

    func = operations.get(operation)

    if func is None:
        return {"error": f'Unknown operation: {operation}'}

    try:
        return func(**args)
    except Exception as e:
        return {"error": e}


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
        return {"error": f'File does not exist: {path}'}

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
