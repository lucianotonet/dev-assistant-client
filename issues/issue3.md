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