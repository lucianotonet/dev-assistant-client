import unittest
import os
from dev_assistant_client.modules import terminal

class TestCD(unittest.TestCase):
    def setUp(self):
        self.original_dir = os.getcwd()

    def tearDown(self):
        os.chdir(self.original_dir)

    def test_cd(self):
        terminal.execute('cd', {'directory': 'D:\\www\\dev-assistant-client\\dev_assistant_client'})
        self.assertEqual(os.getcwd(), 'D:\\www\\dev-assistant-client\\dev_assistant_client')

if __name__ == '__main__':
    unittest.main()