
import pytest
import os

from dev_assistant_client.modules.terminal import execute

def test_execute_run_command():
    # Test running a valid command
    result = execute('run', {'command': "echo 'Hello, world!'"})
    assert 'Hello, world!' in result['stdout']
    assert result['stderr'] == ''

    # Test running an invalid command
    result = execute('run', {'command': 'invalid_command'})
    assert result['stdout'] == ''
    assert 'invalid_command' in result['stderr']
    
    # Test changing directory
    result = execute('run', {'command': 'pwd && cd dev_assistant_client/modules/ && pwd'})
    assert 'modules' in result['stdout']
    
    # Test changing directory to an invalid directory
    result = execute('run', {'command': 'cd invalid_directory'})
    assert result['stdout'] == ''
    assert result['stderr'] != '' # Can be either 'No such file or directory' or 'The system cannot find the path specified.'
    
    # # Test changing directory in separate commands
    # result1 = execute('run', {'command': 'pwd && cd ../'})
    # result2 = execute('run', {'command': 'pwd'})  # Should be the same as result1
    # assert result1['stdout'] != result2['stdout']