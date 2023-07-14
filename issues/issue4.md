# Issue 4

Em PluginController linha 20 nós informamos os argumentos aceitos mas não temos como informar o tipo de cada argumento, então o usuário pode passar qualquer coisa.
No exemplo abaixo o usuário deve iformar mode como "w" ou "a" mas ele pode informar qualquer coisa. Precisamos de uma forma de definir os argumetnos e seus tipos para que sejam informados no openapi schema.
Vide 'dev-assistant-server\app\Http\Controllers\PluginController.php' e também 'dev-assistant-client\dev_assistant_client\modules\files.py'

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

Basic plan

When trying to use files module, we get for example "invalid mode: 'update'".
We need to validate commands but just 'r', 'w', 'a' are the only valid modes today.

- Fix validation on commands at files module
- Add tests for files module
