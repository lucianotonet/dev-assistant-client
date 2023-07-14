from dev_assistant_client.modules.terminal import execute
import pytest
import os

def test_execute_run_command():
    # Test running a valid command
    result = execute('run', {'command': "echo 'Hello, world!'"})
    assert result['stdout'] == "'Hello, world!'\n"
    assert result['stderr'] == ''

    # Test running an invalid command
    result = execute('run', {'command': 'invalid_command'})
    assert result['stdout'] == ''
    assert 'invalid_command' in result['stderr']        

    # Test changing the current directory
    result = execute('run', {'command': 'pwd'})
    current_dir = os.path.normpath(
        os.path.abspath(os.getcwd())).replace('\\', '/')
    current_dir = '/' + current_dir.replace(':', '')  # Convert to Unix format
    assert result['stdout'].strip().lower() == current_dir.lower()

    # Test running a command with a relative path
    result = execute('run', {'command': 'ls ../'})
    assert 'dev-assistant-client' in result['stdout']

    # Test running a command with an absolute path
    result = execute('run', {'command': 'ls /'})
    assert 'bin' in result['stdout']
