import os

def execute(operation, args):
    if operation == 'create_file':
        return create_file(args.get('path'), args.get('content'))
    elif operation == 'read_file':
        return read_file(args.get('path'))
    elif operation == 'update_file':
        return update_file(args.get('path'), args.get('content'), args.get('mode'))
    elif operation == 'delete_file':
        return delete_file(args.get('path'))
    elif operation == 'list_directory':
        return list_directory(args.get('path'))
    else:
        return {'error': f'Unknown operation: {operation}'}

def create_file(path, content=None):
    try:
        # Check if directory exists, if not create it
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'w', encoding='utf-8') as file:
            if content:
                file.write(content)
        return {"message": f"File created at {path}"}
    except Exception as e:
        return {"error": str(e)}

def read_file(path):
    try:
        with open(path, 'r') as file:
            content = file.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

def update_file(path, content, mode='a'):
    try:
        with open(path, mode, encoding='utf-8') as file:
            file.write(content)
        return {"message": f"File updated at {path}"}
    except Exception as e:
        return {"error": str(e)}

def delete_file(path):
    try:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
        return {"message": f"File or directory deleted at {path}"}
    except Exception as e:
        return {"error": str(e)}

def list_directory(path):
    try:
        files = os.listdir(path)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

def create_directory(path):
    try:
        if os.path.isdir(path):
            return {"message": f"Directory already exists at {path}"}
        else:
            os.mkdir(path)
            return {"message": f"Directory created at {path}"}
    except Exception as e:
        return {"error": str(e)}