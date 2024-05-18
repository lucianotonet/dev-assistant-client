# Dev Assistant

Bem-vindo ao projeto [Dev Assistant](https://devassistant.tonet.dev).

## O que é?

[Dev Assistant CLI] é um CLIENT do Dev Assistant.
O Dev Assistant CLI é um script python que ao ser iniciado no seu ambiente de desenvolvimente, ele autentica e conecta-se ao servidor Dev Assistant em [https://devassistant.tonet.dev](https://devassistant.tonet.dev), e então fica aguardando por instruções. Quando recebe instruções, o Dev Assistant CLI executa-as através de suas ferramentas no ambiente onde está sendo executado, e então envia a resposta de volta.

Além do cliente CLI em Python existe uma [Extensão para VSCode disponível](https://marketplace.visualstudio.com/items?itemName=LucianoTonet.dev-assistant-ai). 

## Funcionalidades

O Dev Assistant CLI foi projetado trabalhar como ferramenta para assistente de IA,  oferecendo três robustos módulos que executam diretamente no ambiente de desenvolvimento:

- **Gerenciamento de Arquivos**: Criar, ler, atualizar e excluir arquivos. Listar o conteúdo de um diretório. Você pode gerenciar seus arquivos sem sair da conversa com o Dev Assistant GPT.

- **Controle de Versão Git**: Inicializar um repositório Git, adicionar alterações à área de preparação, confirmar alterações e enviar alterações para um repositório remoto. Obter o status do repositório Git. Você pode gerenciar seus repositórios Git diretamente através do Dev Assistant.

- **Execução de Comandos no Terminal**: Executar comandos diretamente no terminal. Você pode executar qualquer comando no seu terminal diretamente do Dev Assistant GPT.

## Requisitos

- 📓 Python 3.10+
- 📓 Pip e Poetry
- ⭐ [Conta do Dev Assistant](https://devassistant.tonet.dev)

## Instalação

- Crie uma conta no Dev Assistant em [devassistant.tonet.dev](https://devassistant.tonet.dev)
- Gere um token em [https://devassistant.tonet.dev/user/api-tokens](https://devassistant.tonet.dev/user/api-tokens) para o Dev Assistant GPT e salve-o. Você vai precisar dele mais tarde.
- Instale o cliente local:
  - [Instale o Poetry](https://python-poetry.org/docs/#installation)
  - Execute `poetry install` para instalar o pacote e suas dependências

## Uso

Once installed, just run the following:

```bash
poetry run dev-assistant
```

If the CLI is not already authenticated, it will open a browser window where you will be provided with a token. Copy the token including the pipe, and return to the terminal.

If everything runs well, you will see the Dev Assistant CLI presentation and a unique _CLIENT ID_, like this:

```

        ╭─────╮   Dev Assistant
        │ >_< │   v0.2.46
        ╰─────╯   https://devassistant.tonet.dev

›       Connecting...           Connected!
›       CLIENT ID:              6a35a11c-f34e-4e30-be46-a9ac4d0f5ac7
›       WebSockets...           Connected!
›       Private channel...      Connected!
›       Ready!  Listening for instructions...
›       

```

You can stop the client just doing a `CRTL+C` in the terminal at any time.

## Commands

Go to [Dev Assistant GPT](https://chat.openai.com/g/g-Qa01WfuKG-dev-assistant) and start a conversation. You can ask for help with the commands, or just let Dev Assistant GPT discover it by itself. It will ask you to login if you are not already logged in.

You can now ask Dev Assistant GPT to do things like:

- Create a new file called `my-file.txt` on my Desktop
- Read a file called `other-file.yml`
- Update a file
- Delete a file
- List the contents of a directory
- Initialize a Git repository
- Add changes to the staging area
- Commit changes
- Push changes to a remote repository
- Get the status of the Git repository
- Execute a command in the terminal
... and more!

## Versioning

To update the version of the package, follow these steps:

1. Commit your changes with a descriptive message.
2. Create a git tag with the format `vX.Y.Z` where `X.Y.Z` is the new version number.
3. Push your changes and the new tag to the repository.

The GitHub Actions workflow will automatically deploy the new version to PyPi when a new tag is detected.

## Contributing

We welcome contributions! If you have an idea for an improvement or have found a bug, please open an issue. Feel free to fork the repository and submit a pull request if you'd like to contribute code. Please follow the code style and conventions used in the existing codebase.

## Development

- Fork the repository
- Clone your fork
- Go to the project folder
- Install Dev Assistant Client in local mode with `poetry install`
- Run `poetry run dev-assistant` in your terminal to start the CLI.
- Make your changes
- Test your changes
- Commit your changes
- Push your changes
- Open a pull request
- 🎉

## License

The Dev Assistant Local Client is open-source software, licensed under the [MIT license](LICENSE).

## Support

If you encounter any problems or have any questions, don't hesitate to open an issue on GitHub. We're here to help!

## Acknowledgements

A big thank you to all contributors and users for your support! We couldn't do it without you.

## Authors

- [Luciano T.](https://github.com/lucianotonet)
- ...