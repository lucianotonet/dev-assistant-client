# Issue 1

## Large File Handling

When sending large files over the network, we encounter a size limit. The current solution is to encode the file content in base64, but this still has a limit and is not the most efficient solution.

### Proposed Solution

1. **Use git diffs:** If the file is being tracked by git, we can generate a diff of the changes and send this diff to the server instead of the entire file. This can significantly reduce the amount of data that needs to be sent, especially if only small changes have been made to the file. However, this approach requires the server to have a copy of the previous state of the file, and it won't work if the file is not being tracked by git.

2. **Base64 encoding with conditional decoding:** If the file is not being tracked by git or is too large to send even with git diffs, we can fall back to the current solution of base64 encoding. However, we should add a condition to check if the file content is base64 encoded and decode it if necessary. This can be done by checking if the file content starts with the base64 prefix.

### Limitations

The base64 encoding solution has a size limit of around 2MB. If the file is larger than this, the encoding will fail. The git diff solution does not have this size limit, but it requires the file to be tracked by git and the server to have a copy of the previous state of the file.

### Next Steps

1. Implement the git diff solution and test it with various file sizes and types.
2. Implement the conditional base64 decoding and test it with various file sizes and types.
3. Determine the maximum file size that can be handled with each solution and document this in the code and user documentation.

# Issue 2

## Issue Description:

We are facing an issue with the 'cd' command in the Dev Assistant client. The issue is that the current directory is being reset to the original directory after the execution of the 'cd' command. This suggests that the update of the terminal state is not working as expected.

The expected behavior is that the 'cd' command changes the current directory and the new directory persists for the subsequent commands. However, what we are observing is that the current directory is being reset to the original directory after the execution of the 'cd' command.

We have tried several approaches to solve this issue, including trying to update the terminal state after the execution of the 'cd' command and running each command in a new shell process that starts in the desired directory. However, none of these approaches have solved the issue.

This issue is critical for the functionality of the Dev Assistant client as it prevents the execution of commands in the desired directory. This can affect the ability of the client to perform tasks such as reading and writing files in specific directories.

We need to investigate this issue further to understand what is causing it and how it can be resolved. This may involve adding more logs to the code to track the execution flow, checking the environment in which the code is being run to ensure it supports changing the directory, and checking for any configuration or restriction in the environment that is preventing the change of directory.

# Issue 3

```
ERROR:ably.rest.auth:Need a new token but auth_options does not include a way to request one
NoneType: None
ERROR:ably.transport.websockettransport:WebSocketTransport.on_protocol_message(): An exception                                 occurred during reauth: 40171 403 Need a new token but auth_options does not include a way to request one
Traceback (most recent call last):
  File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\transport\websockettransport.py", line 123, in on_protocol_message
    await self.connection_manager.ably.auth.authorize()
  File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\rest\auth.py", line 152, in authorize
    return await self.__authorize_when_necessary(token_params, auth_options, force=True)
File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\rest\auth.py", line 101, in__authorize_when_necessary
    token_details = await self._ensure_valid_auth_credentials(token_params, auth_options, force)
File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\rest\auth.py", line 128, in_ensure_valid_auth_credentials
    self.__token_details = await self.request_token(token_params, **auth_options)
  File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\rest\auth.py", line 199, in request_token
    raise AblyAuthException(msg, 403, 40171)
ably.util.exceptions.AblyAuthException: 40171 403 Need a new token but auth_options does not include a way to request one
ERROR:ably.rest.auth:Need a new token but auth_options does not include a way to request one
NoneType: None
```

# Issue 4

Em PluginController linha 20 nós informamos os argumentos aceitos mas não temos como informar o tipo de cada argumento, então o usuário pode passar qualquer coisa.
No exemplo abaixo o usuário deve iformar mode como "w" ou "a" mas ele pode informar qualquer coisa. Precisamos de uma forma de definir os argumetnos e seus tipos para que sejam informados no openapi schema.
Vide D:\www\dev-assistant-server\app\Http\Controllers\PluginController.php e também D:\www\dev-assistant-client\dev_assistant_client\modules\file_management.py

REQUEST TO DEV ASSISTANT
{
  "device": "999c54f7-7993-4b64-ae92-ec51688339bd",
  "args": {
    "path": "path_to_file",
    "content": " ... ",
    "mode": "overwrite"
  }
}
RESPONSE FROM DEV ASSISTANT
{
  "error": "invalid mode: 'overwrite'"
}
