import unittest
from dev_assistant_client.io import get_module_instructions


class TestInstructions(unittest.TestCase):
    def test_get_module_instructions(self):
        modules = ['files', 'git', 'terminal']
        for module in modules:
            instructions = get_module_instructions(module)
            self.assertIsNotNone(instructions)
            self.assertIsInstance(instructions, str)


if __name__ == '__main__':
    unittest.main()