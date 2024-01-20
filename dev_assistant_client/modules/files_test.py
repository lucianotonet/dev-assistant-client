import os
from files import FilesModule

class TestFilesModule:

    def setup_method(self):
        instruction = {
            "module": "files",
            "command": "create",
            "args": ["test.txt"]
        }
        self.module = FilesModule(instruction)

    def test_create(self):
        self.module.create('test.txt')
        assert os.path.exists('test.txt')

    def test_read(self):
        self.module.create('test.txt', 'Hello, world!')
        assert self.module.read('test.txt') == 'Hello, world!'

    def test_update(self):
        self.module.create('test.txt', 'Hello, world!')
        self.module.update('test.txt', 'Goodbye, world!')
        assert self.module.read('test.txt') == 'Goodbye, world!'

    def test_append(self):
        self.module.create('test.txt', 'Hello, world!')
        self.module.append('test.txt', 'Goodbye, world!')
        assert self.module.read('test.txt') == 'Hello, world!Goodbye, world!'

    def test_delete(self):
        self.module.create('test.txt')
        self.module.delete('test.txt')
        assert not os.path.exists('test.txt')

    def test_list_dir(self):
        self.module.create('test.txt')
        self.module.create('test2.txt')
        assert self.module.list_dir('.') == ['test.txt', 'test2.txt']

    def test_copy(self):
        self.module.create('test.txt', 'Hello, world!')
        self.module.copy('test.txt', 'test2.txt')
        assert os.path.exists('test2.txt')
        assert self.module.read('test2.txt') == 'Hello, world!'

    def test_move(self):
        self.module.create('test.txt', 'Hello, world!')
        self.module.move('test.txt', 'test2.txt')
        assert not os.path.exists('test.txt')
        assert os.path.exists('test2.txt')
        assert self.module.read('test2.txt') == 'Hello, world!'

    def test_rename(self):
        self.module.create('test.txt', 'Hello, world!')
        self.module.rename('test.txt', 'test2.txt')
        assert not os.path.exists('test.txt')
        assert os.path.exists('test2.txt')
        assert self.module.read('test2.txt') == 'Hello, world!'

    def test_apply_diff(self):
        self.module.create('test.txt', 'Hello, world!')
        diff_instructions = """
--- a/test.txt
+++ b/test.txt
@@ -1,1 +1,1 @@
Hello, world!
Goodbye, world!
"""
        self.module.apply_diff('test.txt', diff_instructions)
        assert self.module.read('test.txt') == 'Goodbye, world!'

    def test_exists(self):
        self.module.create('test.txt')
        assert self.module.exists('test.txt')

    def test_is_file(self):
        self.module.create('test.txt')
        assert self.module.is_file('test.txt')

    def test_is_dir(self):
        self.module.create_directory('test_dir')
        assert self.module.is_dir('test_dir')

    def test_get_size(self):
        self.module.create('test.txt', 'Hello, world!')
        assert self.module.get_size('test.txt') == 13

    def test_create_directory(self):
        self.module.create_directory('test_dir')
        assert os.path.exists('test_dir')

    def test_set_permissions(self):
        self.module.create('test.txt')
        self.module.set_permissions('test.txt', 0o777)
        assert os.stat('test.txt').st_mode == 0o777


