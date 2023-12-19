class FilesModule:
    import os
    import shutil
    import unidiff

    def __init__(self):
        self.operations = {
            "create": self.create,
            "read": self.read,
            "update": self.update,
            "delete": self.delete,
            "list": self.list_dir,
            "copy": self.copy,
            "move": self.move,
            "rename": self.rename,
            "apply_diff": self.apply_diff,
            "exists": self.exists,
            "is_file": self.is_file,
            "is_dir": self.is_dir,
            "get_size": self.get_size
        }
    
    def execute(self, operation, arguments):
        operation_func = self.operations.get(operation)
        if operation_func:
            return operation_func(arguments)
        else:
            return {'error': f'Unknown operation: {operation}. Available operations: {", ".join(self.operations.keys())}'}

    def create(self, arguments):
        path, content = arguments.split(',')
        directory = self.os.path.dirname(path)
        if not self.os.path.exists(directory):
            self.os.makedirs(directory)

        with open(path, "w", encoding="utf-8") as file:
            if content:
                file.write(content)
        return {"message": f"File created at {path}"}

    def read(self, path):
        if not self.os.path.exists(path):
            return {"error": f"Path does not exist: {path}"}

        if self.os.path.isdir(path):
            return self.list_dir(path)

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        return {"content": content}

    def update(self, arguments):
        path, content = arguments.split(',')
        if not self.os.path.exists(path):
            return {"error": f"File does not exist: {path}"}

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return {"message": f"File updated at {path}"}

    def delete(self, path):
        if not self.os.path.exists(path):
            return {"error": f"File does not exist: {path}"}

        self.os.remove(path)
        return {"message": f"File deleted at {path}"}

    def list_dir(self, path):
        if not self.os.path.exists(path):
            return {"error": f"Directory does not exist: {path}"}

        try:
            files = self.os.listdir(path)
        except Exception as e:
            return {"error": f"Error listing directory: {e}"}
        
        return {"files": files}

    def copy(self, arguments):
        source, destination = arguments.split(',')
        if not self.os.path.exists(source):
            return {"error": f"File does not exist: {source}"}

        self.shutil.copy(source, destination)
        return {"message": f"File copied from {source} to {destination}"}

    def move(self, arguments):
        source, destination = arguments.split(',')
        if not self.os.path.exists(source):
            return {"error": f"File does not exist: {source}"}

        self.shutil.move(source, destination)
        return {"message": f"File moved from {source} to {destination}"}

    def rename(self, arguments):
        source, destination = arguments.split(',')
        if not self.os.path.exists(source):
            return {"error": f"File does not exist: {source}"}

        self.os.rename(source, destination)
        return {"message": f"File renamed from {source} to {destination}"}

    def apply_diff(self, arguments):
        path, diff_instructions = arguments.split(',')
        if not self.os.path.exists(path):
            return {"error": f"File does not exist: {path}"}

        with open(path, "r", encoding="utf-8") as file:
            original_content = file.read()

        # Apply diff instructions using unidiff
        patch_set = self.unidiff.PatchSet.from_string(diff_instructions)
        patched_content = original_content
        for patched_file in patch_set:
            for hunk in patched_file:
                patched_content = hunk.apply_to(patched_content)

        # Save the file after applying the diff
        with open(path, "w", encoding="utf-8") as file:
            file.write(patched_content)

        return {"message": f"Diff applied to file at {path}"}

    def exists(self, path):
        return {"exists": self.os.path.exists(path)}

    def is_file(self, path):
        return {"is_file": self.os.path.isfile(path)}

    def is_dir(self, path):
        return {"is_dir": self.os.path.isdir(path)}

    def get_size(self, path):
        return {"size": self.os.path.getsize(path)}