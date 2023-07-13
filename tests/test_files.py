import os
import pytest
from dev_assistant_client.modules.files import execute, create_file, read_file, update_file, delete_file, list_directory, create_directory

@pytest.fixture
def file_path(tmpdir):
    file = tmpdir.join("test.txt")
    file.write("test content")
    return str(file)

@pytest.fixture
def dir_path(tmpdir):
    dir = tmpdir.mkdir("test_dir")
    return str(dir)

def test_create_file(file_path):
    result = create_file(file_path, "new content")
    assert result == {"message": f"File created at {file_path}"}
    with open(file_path, "r") as f:
        assert f.read() == "new content"

def test_read_file(file_path):
    result = read_file(file_path)
    assert result == {"content": "test content"}

def test_update_file(file_path):
    result = update_file(file_path, "updated content")
    assert result == {"message": f"File updated at {file_path}"}
    with open(file_path, "r") as f:
        assert f.read() == "test contentupdated content"

def test_delete_file(file_path):
    result = delete_file(file_path)
    assert result == {"message": f"File or directory deleted at {file_path}"}
    assert not os.path.exists(file_path)

def test_list_directory(dir_path):
    result = list_directory(dir_path)
    assert result == {"files": []}

def test_create_directory(dir_path):
    result = create_directory(dir_path)
    assert result == {"message": f"Directory already exists at {dir_path}"}
    new_dir_path = os.path.join(dir_path, "new_dir")
    result = create_directory(new_dir_path)
    assert result == {"message": f"Directory created at {new_dir_path}"}
    assert os.path.exists(new_dir_path)