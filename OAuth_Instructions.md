A/C ChatGPT

# Instruções para Implementação de Autenticação OAuth no Cliente Python

## Contexto

O objetivo é permitir que os usuários do cliente Python se autentiquem usando OAuth, especificamente através do GitHub, sem inserir diretamente suas credenciais no cliente. Em vez disso, eles serão redirecionados para a página de login do aplicativo web, onde podem se autenticar e, em seguida, receber um token para usar no cliente Python.

## Passos

1. **Iniciar o Cliente Python**:
   - Ao iniciar o cliente Python, verifique se já possui um token válido.
   - Se não tiver um token válido, informe ao usuário que ele precisa se autenticar.

2. **Redirecionar para o Navegador ou Mostrar o Link**:
   - Abra automaticamente o navegador padrão do usuário e redirecione-o para a página de login do aplicativo web.
   - Alternativamente, mostre ao usuário um link para a página de login e peça que ele abra esse link em seu navegador.

3. **Login via Web**:
   - O usuário faz login no aplicativo web usando o GitHub ou qualquer outro método de autenticação disponível.

4. **Retorno ao Cliente Python**:
   - Após o login bem-sucedido, o aplicativo web gera um token e exibe esse token ao usuário com instruções para copiá-lo e colá-lo de volta no cliente Python.

5. **Inserir Token no Cliente Python**:
   - O usuário copia o token da página web e insere no cliente Python.
   - O cliente Python usa esse token para todas as chamadas de API subsequentes.

6. **Armazenar Token**:
   - O cliente Python armazena o token localmente (de forma segura) para que o usuário não precise repetir esse processo toda vez que iniciar o cliente.

## Considerações Adicionais

- Certifique-se de que o token seja armazenado de forma segura no cliente Python, possivelmente usando um armazenamento de credenciais do sistema operacional.
- O aplicativo web deve ter uma interface clara para mostrar o token ao usuário após o login bem-sucedido, com instruções claras sobre como copiá-lo e onde inseri-lo no cliente Python.
- O cliente Python deve ter uma maneira fácil de inserir o token, e também uma opção para 'deslogar' ou invalidar o token atual.
- Temos também uma extensão para vscode que está sendo desenvolvida e precisará de suporte para autenticação OAuth. O fluxo de trabalho será semelhante ao do cliente Python.
- O código-fonte do servidor, feito em Laravel com Jetstream, está disponível em [lucianotonet/dev-assistant-server](https://github.com/lucianotonet/dev-assistant-server) (privado) e está clonado em D:\www\dev-assistant-server no mesmo device. O mesmo é acessível em [devassistant.tonet.dev](https://devassistant.tonet.dev) em produção.