import os
import shutil
import unittest
from git import Repo
from dev_assistant_client.modules.git import execute


class TestGit(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'test_repo')

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_git_init(self):
        result = execute('init', {'directory': self.test_dir})
        self.assertEqual(result['message'], f"Repo init in {self.test_dir}")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, '.git')))

    def test_git_add(self):
        repo = Repo.init(self.test_dir)
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('test')
        result = execute('add', {'directory': self.test_dir})
        self.assertEqual(result['message'], f"Repo add in {self.test_dir}")
        self.assertIn('test.txt', repo.git.status())

    def test_git_commit(self):
        repo = Repo.init(self.test_dir)
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('test')
        repo.git.add('.')
        result = execute(
            'commit', {'message': 'test commit', 'directory': self.test_dir})
        self.assertEqual(result['message'], f"Repo commit in {self.test_dir}")
        self.assertIn('test commit', repo.git.log())    

    def test_git_status(self):
        repo = Repo.init(self.test_dir)
        with open(os.path.join(self.test_dir, 'test.txt'), 'w') as f:
            f.write('test')
        repo.git.add('.')
        result = execute('status', {'directory': self.test_dir})
        self.assertEqual(result['message'], f"Repo status in {self.test_dir}")
        self.assertIn('test.txt', result['status'])

    def test_git_diff(self):
        repo = Repo.init(self.test_dir)
        file_path = os.path.join(self.test_dir, 'test.txt')
        with open(file_path, 'w') as f:
            f.write('test')
        repo.git.add('.')
        repo.git.commit('-m', 'Initial commit')
        with open(file_path, 'a') as f:
            f.write('\nMore test content')
        repo.git.add('.')
        result = execute(
            'diff', {'file_path': 'test.txt', 'directory': self.test_dir})
        self.assertEqual(result['message'],
                        f"Git diff for test.txt in {self.test_dir}")
        self.assertIn('More test content', result['diff'])
