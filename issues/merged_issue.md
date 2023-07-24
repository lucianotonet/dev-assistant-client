# Issue 3 e Erro de autenticação do Ably

## Descrição da Issue

Durante a execução do projeto, encontramos um erro de autenticação do Ably. O erro indica que o token de autenticação necessário para a conexão com o Ably não está disponível ou expirou, e não há uma maneira configurada para solicitar um novo token.

## Log de erro:
```
ERROR:ably.rest.auth:Need a new token but auth_options does not include a way to request one
NoneType: None
ERROR:ably.transport.websockettransport:WebSocketTransport.on_protocol_message(): An exception                                 occurred during reauth: 40171 403 Need a new token but auth_options does not include a way to request one
Traceback (most recent call last):
  File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\transport\websockettransport.py", line 123, in on_protocol_message
    await self.connection_manager.ably.auth.authorize()
  File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\rest\auth.py", line 152, in authorize
    return await self.__authorize_when_necessary(token_params, auth_options, force=True)
  File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\rest\auth.py", line 101, in __authorize_when_necessary
    token_details = await self._ensure_valid_auth_credentials(token_params, auth_options, force)
  File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\rest\auth.py", line 128, in _ensure_valid_auth_credentials
    self.__token_details = await self.request_token(token_params, **auth_options)
  File "C:\laragon\bin\python\python-3.10\lib\site-packages\ably\rest\auth.py", line 199, in request_token
    raise AblyAuthException(msg, 403, 40171)
ably.util.exceptions.AblyAuthException: 40171 403 Need a new token but auth_options does not include a way to request one
ERROR:ably.rest.auth:Need a new token but auth_options does not include a way to request one
NoneType: None
```

## Passos para reproduzir o problema:
1. (Incluir os passos que levaram ao erro)

## Comportamento esperado:
O sistema deve ser capaz de solicitar um novo token de autenticação quando o atual expirar ou não estiver disponível.

## Comportamento atual:
O sistema não está configurado para solicitar um novo token de autenticação quando o atual expirar ou não estiver disponível.

## Informações do ambiente:
- Sistema operacional: (incluir o sistema operacional)
- Versão do Python: (incluir a versão do Python)
- Outras informações relevantes

## Possível solução:
Investigar a configuração de autenticação do Ably e garantir que uma maneira de solicitar um novo token esteja configurada.