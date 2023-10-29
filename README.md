# Dev Assistant

Welcome to the [Dev Assistant](https://devassistant.tonet.dev) plugin for ChatGPT.

## What is it?

[Dev Assistant](https://devassistant.tonet.dev) is a plugin for ChatGPT that assists us developers by executing tasks directly on our development environment.

Dev Assistant Client (this repo) is a Python package that is basically the core component of the project. It receives instructions from ChatGPT via Dev Assistant plugin, executes it olcoally and send the response back.

## Features

The Dev Assistant Client is designed to streamline your development process by offering a range of functionalities:

- **File Management**: Create, read, update, and delete files. List the contents of a directory. You can manage your files without leaving your conversation with ChatGPT.

- **Git Version Control**: Initialize a Git repository, add changes to the staging area, commit changes, and push changes to a remote repository. Get the status of the Git repository. You can manage your Git repositories directly through ChatGPT.

- **Terminal Commands Execution**: Execute commands directly in the terminal. You can run any command in your terminal directly from ChatGPT.

## Requirements

- 📓 Python 3.10+
- 📓 Pip and Poetry
- 💸 ChatGPT Plus subscription _(for plugins store access)_
- ⭐ [ChatGPT Plugins development access](https://openai.com/waitlist/plugins)

## Installation

- Create a Dev Assistant account at [devassistant.tonet.dev](https://devassistant.tonet.dev)
- Generate a token at [https://devassistant.tonet.dev/user/api-tokens](https://devassistant.tonet.dev/user/api-tokens) for ChatGPT and save it. You will need it later.
- Install the local client:
  - [Install Python](https://www.python.org/downloads/)
  - Run `pip install dev-assistant-client` in your terminal
- Install the ChatGPT plugin:
  - In the [ChatGPT Plugins Store](https://chat.openai.com/plugins), click on **"Install an unverified plugin"** at the bottom of the Plugin store dialog window, paste <https://devassistant.tonet.dev> and click on "Find plugin".
  - ChatGPT will ask you to enter your credentials. Enter the token generated in the second step and click on "Install plugin".
  - Activate the plugin in the list of installed plugins and you are ready to start!

## Usage

Once installed, just run the following:

```bash
dev-assistant
```

If the CLI is not already authenticated, it will open a browser window where you will be provided with a token. Copy the token including the pipe, and return to the terminal.

If everything runs well, you will see the Dev Assistant CLI presentation and a exclusive _CLIENT ID_, like this:

```

        ╭─────╮   Dev Assistant
        │ >_< │   v0.2.34
        ╰─────╯   https://devassistant.tonet.dev

›       Connecting...           Connected!
›       CLIENT ID:              6a35a11c-f34e-4e30-be46-a9ac4d0f5ac7
›       WebSockets...           Connected!
›       Private channel...      Connected!
›       Ready!  Listening for instructions...
›       

```

You can now ask ChatGPT to access your development environment and execute commands on your behalf by passing the _CLIENT ID_, or just let ChatGPT discover it by itself.

You can stop the client just doing a `CRTL+C` in the terminal at any time.

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
- Install Dev Assistant Client in local mode with `pip install -e .`
- Run `dev-assistant` in your terminal
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
- [ChatGPT](https://chat.openai.com/)
- [GitHub Copilot](https://copilot.github.com/)