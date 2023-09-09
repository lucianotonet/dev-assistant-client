import os
import shutil
import unittest
from git import Repo
from unittest.mock import patch, MagicMock
from dev_assistant_client.modules.git_module import execute


class TestGitModule(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'test_repo')

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch('dev_assistant_client.modules.git_module.Repo')
    def test_git_init(self, mock_repo):
        execute('init', {'directory': self.test_dir})
        mock_repo.init.assert_called_once_with(self.test_dir)

    @patch('dev_assistant_client.modules.git_module.Repo')
    def test_git_add(self, mock_repo):
        execute('add', {'directory': self.test_dir})
        mock_repo.assert_called_once_with(self.test_dir)
        mock_repo.return_value.git.add.assert_called_once_with('.')

    @patch('dev_assistant_client.modules.git_module.Repo')
    def test_git_commit(self, mock_repo):
        execute('commit', {'message': 'test commit', 'directory': self.test_dir})
        mock_repo.assert_called_once_with(self.test_dir)
        mock_repo.return_value.git.commit.assert_called_once_with('-m', 'test commit')

    @patch('dev_assistant_client.modules.git_module.Repo')
    def test_git_status(self, mock_repo):
        execute('status', {'directory': self.test_dir})
        mock_repo.assert_called_once_with(self.test_dir)
        mock_repo.return_value.git.status.assert_called_once()

    @patch('dev_assistant_client.modules.git_module.Repo')
    def test_git_diff(self, mock_repo):
        execute('diff', {'file_path': 'test.txt', 'directory': self.test_dir})
        mock_repo.assert_called_once_with(self.test_dir)
        mock_repo.return_value.git.diff.assert_called_once_with('test.txt')


if __name__ == '__main__':
    unittest.main()