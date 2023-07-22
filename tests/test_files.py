import os
import pytest
from dev_assistant_client.modules.files import execute, create, read, update, delete, list_dir

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
    result = create(file_path, "new content")
    assert result == {"message": f"File created at {file_path}"}
    with open(file_path, "r") as f:
        assert f.read() == "new content"

def test_read_file(file_path):
    result = read(file_path)
    assert result == {"content": "test content"}

def test_update_file(file_path):
    result = update(file_path, "updated content")
    assert result == {"message": f"File updated at {file_path}"}
    with open(file_path, "r") as f:
        assert f.read() == "test contentupdated content"

def test_delete_file(file_path):
    result = delete(file_path)
    assert result == {"message": f"File or directory deleted at {file_path}"}
    assert not os.path.exists(file_path)

def test_list_directory(dir_path):
    result = list_dir(dir_path)
    assert result == {"files": []}