
import json
import os
import shutil
import unidiff
import logging
from pathlib import Path
from ..utils import StateManager, dd
        

# Setting up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FilesModule:
    def __init__(self, instruction):
        self.client_id = instruction.get("client_id")
        self.feedback = instruction.get("feedback")
        self.module = instruction.get("module")
        self.operation = instruction.get("operation")
        self.arguments = instruction.get("arguments", [])

        self.state_manager = StateManager()  # Instancia StateManager
        self.state = self.state_manager.get_state()  # Carrega o estado
        
        self.current_dir = self.state.get("cwd", os.getcwd())  # Carrega o diretório atual
        self.operations = {
            "create": self.create,
            "read": self.read,
            "update": self.update,
            "append": self.append,
            "delete": self.delete,
            "list_dir": self.list_dir,
            "copy": self.copy,
            "move": self.move,
            "rename": self.rename,
            "apply_diff": self.apply_diff,
            "exists": self.exists,
            "is_file": self.is_file,
            "is_dir": self.is_dir,
            "get_size": self.get_size,
            "create_directory": self.create_directory,
            "set_permissions": self.set_permissions,
            "api_spec": self.get_api_spec
        }        

    def get_api_spec(self, *args):
        return {
            "module": "Files",
            "operations": {
                "create": {"summary": "Create a file", "parameters": [{"name": "path", "in": "query", "type": "string"}, {"name": "content", "in": "query", "type": "string"}]},
                "read": {"summary": "Read a file", "parameters": [{"name": "path", "in": "query", "type": "string"}], "responses": {"200": {"content": {"application/json": {"schema": {"type": "object", "properties": {"content": {"type": "string"}}}}}}}},
                "update": {"summary": "Update a file", "parameters": [{"name": "path", "in": "query", "type": "string"}, {"name": "content", "in": "query", "type": "string"}]},
                "append": {"summary": "Append content to a file", "parameters": [{"name": "path", "in": "query", "type": "string"}, {"name": "content", "in": "query", "type": "string"}]},
                "delete": {"summary": "Delete a file", "parameters": [{"name": "path", "in": "query", "type": "string"}]},
                "list_dir": {"summary": "List directory contents", "parameters": [{"name": "path", "in": "query", "type": "string"}], "responses": {"200": {"content": {"application/json": {"schema": {"type": "array", "items": {"type": "string"}}}}}}},
                "copy": {"summary": "Copy a file", "parameters": [{"name": "source", "in": "query", "type": "string"}, {"name": "destination", "in": "query", "type": "string"}]},
                "move": {"summary": "Move a file", "parameters": [{"name": "source", "in": "query", "type": "string"}, {"name": "destination", "in": "query", "type": "string"}]},
                "rename": {"summary": "Rename a file", "parameters": [{"name": "source", "in": "query", "type": "string"}, {"name": "destination", "in": "query", "type": "string"}]},
                "apply_diff": {"summary": "Apply a diff to a file", "parameters": [{"name": "path", "in": "query", "type": "string"}, {"name": "diff_instructions", "in": "query", "type": "string"}]},
                "exists": {"summary": "Check if a file or directory exists", "parameters": [{"name": "path", "in": "query", "type": "string"}], "responses": {"200": {"content": {"application/json": {"schema": {"type": "object", "properties": {"exists": {"type": "boolean"}}}}}}}},
                "is_file": {"summary": "Check if a path is a file", "parameters": [{"name": "path", "in": "query", "type": "string"}], "responses": {"200": {"content": {"application/json": {"schema": {"type": "object", "properties": {"is_file": {"type": "boolean"}}}}}}}},
                "is_dir": {"summary": "Check if a path is a directory", "parameters": [{"name": "path", "in": "query", "type": "string"}], "responses": {"200": {"content": {"application/json": {"schema": {"type": "object", "properties": {"is_dir": {"type": "boolean"}}}}}}}},
                "get_size": {"summary": "Get a file size", "parameters": [{"name": "path", "in": "query", "type": "string"}], "responses": {"200": {"content": {"application/json": {"schema": {"type": "object", "properties": {"size": {"type": "integer"}}}}}}}},
                "create_directory": {"summary": "Create a directory", "parameters": [{"name": "path", "in": "query", "type": "string"}]},
                "set_permissions": {"summary": "Set file permissions", "parameters": [{"name": "path", "in": "query", "type": "string"}, {"name": "mode", "in": "query", "type": "string"}]}
            }
        }
    
    def execute(self):
        operation_func = self.operations.get(self.operation, self.unknown_operation)
        try:
            execute_response = operation_func(*self.arguments)
            return json.dumps(execute_response)
        except TypeError as e:
            return json.dumps({'error': f'Invalid arguments for {self.operation}: {str(e)}'}, ensure_ascii=False)
        except FileNotFoundError as e:
            return json.dumps({'error': str(e)}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'error': f'Error in {self.operation}: {str(e)}'}, ensure_ascii=False)
    
    def unknown_operation(self, *args):
        valid_operations = list(self.operations.keys())
        return json.dumps({'error': f'Unknown operation: {self.operation}', 'valid_operations': valid_operations})

    def path_exists(self, path):
        return os.path.exists(path)

    def create(self, path, content=None):
        absolute_path = Path(self.current_dir, path).resolve()
        directory = absolute_path.parent
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        with open(absolute_path, "w", encoding="utf-8") as file:
            if content:
                file.write(content)
        return {"message": f"File created at {absolute_path}"}

    def read(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"Path does not exist: {absolute_path}"}
        if absolute_path.is_dir():
            return self.list_dir(absolute_path)
        with open(absolute_path, "r", encoding="utf-8") as file:
            content = file.read()
        return {"content": content}

    def update(self, path, content):
        if not os.path.exists(path):
            return {"error": f"File does not exist: {path}"}

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return {"message": f"File updated at {path}"}

    def append(self, path, content=""):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}

        with open(absolute_path, "a", encoding="utf-8") as file:
            file.write(content)

        return {"message": f"Content appended to file at {absolute_path}"}
    
    def delete(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}

        os.remove(absolute_path)
        return {"message": f"File deleted at {absolute_path}"}

    def list_dir(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"Directory does not exist: {absolute_path}"}

        try:
            files = os.listdir(str(absolute_path))
            return {"files": files}
        except Exception as e:
            return {"error": f"Error listing directory: {e}"}

    def copy(self, source, destination):
        try:
            absolute_source = Path(self.current_dir, source).resolve()
            absolute_destination = Path(self.current_dir, destination).resolve()
            if not self.path_exists(absolute_source):
                return {"error": f"File does not exist: {absolute_source}"}

            shutil.copy(absolute_source, absolute_destination)
            return {"message": f"File copied from {absolute_source} to {absolute_destination}"}
        except Exception as e:
            return {"error": f"Error copying file: {e}"}

    def move(self, source, destination):
        try:
            absolute_source = Path(self.current_dir, source).resolve()
            absolute_destination = Path(self.current_dir, destination).resolve()
            if not self.path_exists(absolute_source):
                return {"error": f"File does not exist: {absolute_source}"}

            shutil.move(absolute_source, absolute_destination)
            return {"message": f"File moved from {absolute_source} to {absolute_destination}"}
        except Exception as e:
            return {"error": f"Error moving file: {e}"}

    def rename(self, source, destination):
        try:
            absolute_source = Path(self.current_dir, source).resolve()
            absolute_destination = Path(self.current_dir, destination).resolve()
            if not self.path_exists(absolute_source):
                return {"error": f"File does not exist: {absolute_source}"}

            os.rename(absolute_source, absolute_destination)
            return {"message": f"File renamed from {absolute_source} to {absolute_destination}"}
        except Exception as e:
            return {"error": f"Error renaming file: {e}"}

    def apply_diff(self, path, diff_instructions):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}

        with open(absolute_path, "r", encoding="utf-8") as file:
            original_content = file.read()

        # Apply diff instructions using unidiff
        patch_set = unidiff.PatchSet.from_string(diff_instructions)
        patched_content = original_content
        for patched_file in patch_set:
            for hunk in patched_file:
                patched_content = hunk.apply_to(patched_content)

        # Save the file after applying the diff
        with open(absolute_path, "w", encoding="utf-8") as file:
            file.write(patched_content)

        return {"message": f"Diff applied to file at {absolute_path}"}

    def exists(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        return {"exists": self.path_exists(absolute_path)}

    def is_file(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        return {"is_file": self.path_exists(absolute_path) and os.path.isfile(absolute_path)}

    def is_dir(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        return {"is_dir": self.path_exists(absolute_path) and os.path.isdir(absolute_path)}

    def get_size(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}
        return {"size": os.path.getsize(absolute_path)}

    def create_directory(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        absolute_path.mkdir(parents=True, exist_ok=True)
        return {"message": f"Directory created at {absolute_path}"}

    def set_permissions(self, path, mode):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}
        os.chmod(absolute_path, mode)
        return {"message": f"Permissions set for {absolute_path}"}


