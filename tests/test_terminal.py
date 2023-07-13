import os
import pytest
from dev_assistant_client.modules.terminal import execute


def test_execute_run_command():
    # Test running a valid command
    result = execute('run', {'command': 'echo "Hello, world!"'})
    assert result['stdout'] == 'Hello, world!\n'
    assert result['stderr'] == ''

    # Test running an invalid command
    result = execute('run', {'command': 'invalid_command'})
    assert 'command not found' in result['stderr']

    # Test changing the current directory
    result = execute('run', {'command': 'cd .. && pwd'})
    assert result['stdout'].strip() == os.path.dirname(os.getcwd())

    # Test running a command with a relative path
    result = execute('run', {'command': 'ls ../'})
    assert 'dev-assistant-client' in result['stdout']

    # Test running a command with an absolute path
    result = execute('run', {'command': 'ls /'})
    assert 'bin' in result['stdout']