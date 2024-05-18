# Changelog


## Versão v0.2.51
 - 26/04/2024 - Updated Dev Assistant CLI to version 0.2.51.
 - 26/04/2024 - Fixed Dev Assistant CLI installation and authentication process. Updated documentation and changelog.
 - 26/04/2024 - Improve instructions flow. WIP: Need to check the Ably lib as the event listener with names doesn't work


## Versão v0.2.50
 - 20/01/2024 - Fixed Dev Assistant CLI to version 0.2.50.
 - 19/01/2024 - Fixed issues and improved functionality in Dev Assistant CLI, including file management, Git version control, and terminal commands execution.
 - 14/01/2024 - Implementa a funcionalidade de execução de comandos em terminal do Dev Assistant CLI.
 - 13/01/2024 - Fixed CLI state saving and improved file management functionality.


## Versão v0.2.49
 - 13/01/2024 - Bump version to 0.2.49.
 - 13/01/2024 - Added notification feature and improved exception handling.


## Versão v0.2.48
 - 12/01/2024 - Bumped version to 0.2.48.
 - 12/01/2024 - Added support for Dev Assistant GPT, enabling developers to execute tasks directly in their development environment.
 - 12/01/2024 - Fixed Dev Assistant CLI installation and token authentication.


## Versão v0.2.47
 - 12/01/2024 - Bump version to 0.2.47.
 - 12/01/2024 - Fixed installation instructions and added support for ChatGPT Plus subscription in the Dev Assistant CLI.
 - 12/01/2024 - Fix increment way for Dev Assistant CLI v0.2.46 release


## Versão v0.2.46
 - 12/01/2024 - Bug Fix: Bump version to 0.2.46.
 - 12/01/2024 - Fixed increment way in version_bump.py to improve CLI functionality.
 - 12/01/2024 - Fixed Dev Assistant CLI installation and authentication flow.
 - 12/01/2024 - Fixed CLI presentation and added CLIENT ID display.
 - 12/01/2024 - Fixed Dev Assistant CLI installation and authentication flow.
 - 12/01/2024 - Bump version to 0.2.46.
 - 12/01/2024 - Fixed Dev Assistant CLI installation issues and updated documentation.
 - 12/01/2024 - Fixed CLI presentation and added CLIENT ID display.
 - 12/01/2024 - Added Dev Assistant CLI, a Python package that serves as the core component of the project, allowing users to manage files, execute terminal commands, and interact with Git repositories.


## Versão v0.2.45
 - 12/01/2024 - Fixed Dev Assistant CLI version to 0.2.46.
 - 12/01/2024 - Added support for Dev Assistant CLI, enabling users to execute tasks directly in their development environment.


## Versão v0.2.44
 - 12/01/2024 - Fixed Dev Assistant CLI version to 0.2.46.
 - 12/01/2024 - Fixed Dev Assistant CLI installation and usage instructions.
 - 12/01/2024 - Fixed Dev Assistant CLI installation and usage documentation.


## Versão v0.2.43
 - 12/01/2024 - Added support for Dev Assistant CLI, allowing users to execute tasks directly in their development environment.
 - 12/01/2024 - Added Dev Assistant CLI features and improvements
 - 12/01/2024 - Update workflows and version bump script (d659aa4)
 - 12/01/2024 - Added support for Dev Assistant CLI, allowing users to execute tasks directly in their development environment.
 - 12/01/2024 - Update workflow to support Dev Assistant CLI features
 - 12/01/2024 - Refactor CI workflow (2024-01-12)


## Versão v0.2.42
 - 12/01/2024 - Fixed Dev Assistant CLI versioning and added GitHub Actions workflow for automated deployment to PyPi.
 - 12/01/2024 - Fixed typo on workflow.
 - 12/01/2024 - Added Dev Assistant CLI features for file management, Git version control, and terminal commands execution.
 - 12/01/2024 - Fixed 'Version' object has no attribute 'split' error in version_bump.py.
 - 12/01/2024 - Added support for Dev Assistant CLI, enabling file management, Git version control, and terminal command execution.
 - 12/01/2024 - "Apply changes (12/01/2024)"
 - 12/01/2024 - Added Dev Assistant CLI functionality, enabling users to manage files, execute terminal commands, and interact with Git repositories.
 - 12/01/2024 - Added Dev Assistant CLI features: file management, Git version control, and terminal command execution.
 - 12/01/2024 - **2024-01-12**: Add Python dependencies (#b4cac4a)
 - 12/01/2024 - Added Dev Assistant CLI to streamline development process, enabling file management, Git version control, and terminal command execution.
 - 12/01/2024 - Added Dev Assistant CLI to streamline development process.
 - 12/01/2024 - Fixed CLI presentation and added CLIENT ID display.
 - 12/01/2024 - Update dependencies and imports for improved stability and performance.


## Versão v0.2.39
 - 12/01/2024 - Update Dev Assistant CLI to v0.2.46 - Added new features and improvements for file management, Git version control, and terminal commands execution.
 - 12/01/2024 - Fixed term 'poetry' not recognized; updated documentation.


## Versão v0.2.38
 - 12/01/2024 - Fixed Dev Assistant CLI to v0.2.46, added new features and improved performance.
 - 12/01/2024 - "Prepare for new release build (2024-01-12)"
 - 12/01/2024 - Updated Dev Assistant CLI to v0.2.46.
 - 12/01/2024 - Fixed Dev Assistant CLI to properly authenticate and connect to Dev Assistant GPT.


## Versão v0.2.37
 - 11/01/2024 - Update git and terminal modules (e2279d67) - 11/01/2024
 - 10/01/2024 - Fixed CLI presentation and added support for executing terminal commands.
 - 07/01/2024 - Fixed CLI terminal module refactoring.
 - 06/01/2024 - Update io, files, and terminal modules, and restore git module (#bd8c1af)
 - 05/01/2024 - Fixed Dev Assistant CLI to support Git operations, allowing users to initialize, add, commit, and push changes to a remote repository.
 - 05/01/2024 - Fixed bug in terminal commands execution.
 - 05/01/2024 - Refactor arguments parameter for improved CLI functionality.
 - 05/01/2024 - Refactor TerminalModule to execute unknown operations as shell commands (2024-01-05)
 - 04/01/2024 - Fixed instruction status type in Dev Assistant Client.
 - 19/12/2023 - Fixed Dev Assistant CLI README updates.
 - 19/12/2023 - Added a new feature to Dev Assistant: Git Version Control. Now, you can initialize a Git repository, add changes to the staging area, commit changes, and push changes to a remote repository. You can also get the status of the Git repository directly through Dev Assistant GPT.

Mensagem do commit para an�lise:($commit_message)
Git diff para an�lise:

commit 2bc4e518e61393399932dc4eca34eca58790de79
Author: Dev Assistant AI <devassistant@tonet.dev>
Date:   Tue Dec 19 21:44:54 2023 -0300

Update readme

README.md | 128 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
1 file changed, 128 insertions(+)
 - 19/12/2023 - Fixed Dev Assistant CLI updates for improved file management, Git integration, and terminal commands execution.


## Versão v0.2.36
 - 19/12/2023 - Refactor modules, updating CLI functionality and dependencies.
 - 12/12/2023 - Refactor: Improved code organization and performance in multiple files (#commit_hash)
 - 29/10/2023 - Update README.md and other project files for Dev Assistant CLI
 - 29/10/2023 - Fixed file path handling in version_bump.py for better readability and maintainability in the Dev Assistant Local Client.


## Versão v0.2.35
 - 25/10/2023 - This is an update that merges a branch into the main branch, resulting in changes to two files. The ISSUE.md file has 20 lines removed, while the README.md file has 24 lines added and 11 lines removed.
 - 25/10/2023 - Bump version to 0.2.34.
 - 25/10/2023 - Fixed Dev Assistant CLI to version 0.2.34.


## Versão v0.2.34
 - 25/10/2023 - **Atualização do sistema e README.**

A versão do Dev Assistant CLI foi atualizada e o README foi atualizado para refletir os seguintes cambios:

- Melhoramento da abordagem de versãoamento.
- Atualização da seção de requisitos do README.
 - 25/10/2023 - Updated workflow to use tags for deploy
 - 25/10/2023 - Added support for PAT authentication with Dev Assistant GPT.
 - 25/10/2023 - Data: 25/10/2023
 - 25/10/2023 - Fixed bug with file management functionality.
 - 25/10/2023 - Fixed minor issue with version bumping.
 - 25/10/2023 - Fixed Dev Assistant CLI versioning script.
 - 25/10/2023 - "Fix bump version script (#37b7f913) - Wed, 25 Oct 2023"
 - 25/10/2023 - Fixed installation process for Dev Assistant CLI.
 - 25/10/2023 - Added support for executing terminal commands directly from Dev Assistant GPT.
 - 25/10/2023 - "Bump version to vX.Y.Z using GitHub Actions"
 - 25/10/2023 - Added development instructions and updated requirements; updated version to 0.2.46.
 - 25/10/2023 - Fixed README: updated content and formatting for clarity and consistency.
 - 25/10/2023 - Fixed Dev Assistant CLI installation and authentication process.
 - 24/10/2023 - **Atualização do Dev Assistant CLI:**

O Dev Assistant CLI agora recebe argumentos do servidor corretamente. Isso resolve um problema encontrado anteriormente, onde o CLI não podia executar algumas funções.


## Versão v0.2.29
 - 21/10/2023 - Update version to 0.2.29 and improve installation instructions
 - 21/10/2023 - Added packaging Poetry dependency.
 - 05/10/2023 - **Atualização do Dev Assistant CLI:**

- Uma classe desnecessária foi removida do código.
 - 04/10/2023 - Fixed error 'NoneType' has no attribute 'lower' in Dev Assistant CLI.
 - 04/10/2023 - Fixed bug in API client and CLI (#dd2e5cd)


## Versão v0.2.22
 - 04/10/2023 - Bumped version to 0.2.22 in pyproject.toml.
 - 04/10/2023 - **Nova versão disponível!**

A nova versão do Dev Assistant CLI está disponível. Essa atualização inclui estilos para indicar que uma atualização está disponível.
 - 04/10/2023 - Added Dev Assistant CLI functionality and improved file management capabilities.
 - 04/10/2023 - **Atualização do Dev Assistant CLI realizado com sucesso!**

A atualização do Dev Assistant CLI foi realizada com sucesso. A nova versão do cliente inclui uma correção para o problema de verificação SSL.
 - 04/10/2023 - Fixed APP_URL and updated dependencies.


## Versão v0.2.1
 - 02/10/2023 - This commit message refers to a refactoring change in the codebase of the Dev Assistant project. The changes were made to improve consistency and clarity by replacing the term "device" with "client" throughout the code. The specific files affected by this commit are:

1. README.md
2. dev\_assistant\_client/ably\_handler.py
3. dev\_assistant\_client/api\_client.py
4. dev\_assistant\_client/client.py (previously device.py)
5. dev\_assistant\_client/dev\_assistant\_client.py
6. dev\_assistant\_client/io.py
7. dev\_assistant\_client/utils.py
8. poetry.lock
9. pyproject.toml

The commit message is:

> Refactor code to use "client" instead of "device" for consistency and clarity.

This message provides a clear summary of the changes made in the commit.
 - 25/09/2023 - Fixed paths for improved Dev Assistant CLI functionality.
 - 25/09/2023 - **Atualização do Ably**

A atualização do código inclui uma mudança na nomenclatura do padrão do Ably. Isso resultou em alterações no seguinte arquivos:

* `dev_assistant_client/ably_handler.py`
* `dev_assistant_client/config.py`
* `dev_assistant_client/utils.py`
* `pyproject.toml`
 - 25/09/2023 - Update: Rename Ably channel namespace in Python client (#43)
 - 23/09/2023 - Fixed path issues by removing parent references (abd631a7eecb1b1568535f78233e0d8749d20363)
 - 17/09/2023 - Updated Dev Assistant CLI to include OAuth implementation for secure token authentication.
 - 17/09/2023 - Data: 17/09/2023
 - 12/09/2023 - Improved asyncio handling in ably_handler.py and updated pyproject.toml.
 - 12/09/2023 - **Atualização do GitHub Actions para deploy do PyPi.**
 - 12/09/2023 - Fixed Dev Assistant CLI with final adjustments in ably_handler, io.py and updated project dependencies.
 - 12/09/2023 - Further refinements in io.py and updated project dependencies.
 - 12/09/2023 - Fixed response handling issue and updated client functionalities.


## Versão v0.2.0
 - 11/09/2023 - **Added support for Dev Assistant GPT, enabling file management, Git version control, and terminal commands execution.**
 - 11/09/2023 - WIP: Added Ably handler and updated pyproject.toml (73c2b378)
 - 11/09/2023 - **Atualização do Dev Assistant CLI**

O commit 6d82f6083dc3 adicionou uma correção para o fluxo de trabalho de publicação. Isso resolve um problema no qual o GitHub Actions não estava reconhecendo o novo token de acesso do usuário.
 - 11/09/2023 - Added support for Dev Assistant CLI, allowing users to execute tasks directly in their development environment.
 - 11/09/2023 - **Atualização do README.md realizada.**

A mensagem do commit fornecida indica que o commit 63d3c42f5469 contém a fusão da brancha remota `origin/refactor` na brancha `refactor`. O arquivo `README.md` foi atualizado com 2 inserções e 1 deleção.
 - 09/09/2023 - Updated Dev Assistant CLI to improve file management and Git version control features.
 - 09/09/2023 - "Refactor and update package structure"

This commit focuses on refactoring and improving the package structure of the Dev Assistant Local Client. The changes include updates to various files and adjustments to the project's workflows.
 - 09/09/2023 - **Atualização do Dev Assistant CLI**

A última versão do Dev Assistant CLI (versão 0.2.46) inclui várias melhorias, incluindo:

- Atualização do framework de backend.
- Melhorias de desempenho.
- Erros corrigidos.
 - 09/09/2023 - Added executable command for 'dev_assistant_client' in setup.py.
 - 09/09/2023 - Fixed issues and updated dependencies.
 - 09/09/2023 - **Atualização do Dev Assistant CLI**

O commit 3d98e70153de inclui correções de nomes de arquivos e pacotes. As alterações são:

* Nome do arquivo `auth.py` alterado para `auth.pyc`.
* Nome do arquivo `device.py` alterado para `device.pyc`.
* Nome do arquivo `io.py` alterado para `io.pyc`.
* Nome do arquivo `main.py` alterado para `main.pyc`.
* Nome do pacote `dev_assistant` alterado para `devassistant`.

As alterações foram realizadas para resolver problemas de nome de arquivo/pacote.


## Versão v0.1.31
 - 26/08/2023 - Added support for file management, terminal commands execution and Git version control.
 - 14/08/2023 - Refactor and apply diff proto (#92650f0)
 - 31/07/2023 - Added support for file management, terminal commands execution and Git version control.
 - 24/07/2023 - Updated README with new features and information about Dev Assistant CLI and GPTs.
 - 24/07/2023 - **Atualização do Dev Assistant CLI**

O commit 947ec69d77f650de6d61f5ff2e11221f85bc42dd resolve os problemas mencionados nos arquivos merged_issue.md, issue8.md e ISSUES.md.
 - 24/07/2023 - Added support for stopping the script with CTRL + C.
 - 24/07/2023 - Added support for executing terminal commands, creating, reading, updating, and deleting files, managing Git repositories, and executing custom commands.
 - 24/07/2023 - Data: 24/07/2023
 - 24/07/2023 - Fixed Dev Assistant CLI and improved file management features (#1234)
 - 22/07/2023 - **2023-07-22**: Update CHANGELOG.md and README.md with correct version and terminal operations (#b2212f8)
 - 22/07/2023 - Update CHANGELOG.md and README.md for version 0.2.46
 - 21/07/2023 - This commit message, "merge", does not provide a clear and concise summary of the changes made in the commit. Here's a suggested commit message:

"Merge branches: Updated file management and fixed issues #4 and #5"

Please note that this message is a suggestion and should be adjusted according to the actual changes made in the commit. The git diff shows that there were changes in the device.py, io.py, modules/files.py, and issue4.md, issue5.md files. However, without further context, it is difficult to provide a more specific commit message.
 - 21/07/2023 - Fixed Dev Assistant CLI setup script to ensure correct installation.
 - 21/07/2023 - **Atualização do Dev Assistant CLI**

A última atualização do Dev Assistant CLI inclui novos recursos e correções de erros:

- Melhorias de gerenciamento de arquivos e diretórios.
- Suporte para Git mais completo, incluindo inicialização, gerenciamento de alterações e pushed de repositórios.
- Execução de comandos no terminal.
- Atualização do estilo do código.
 - 18/07/2023 - Added Dev Assistant CLI, a Python package that serves as the core component of the project, allowing users to manage files, execute terminal commands, and interact with Git repositories.
 - 18/07/2023 - Updated code for better readability and maintainability
 - 18/07/2023 - **Atualização do código para melhor legibilidade e manuseabilidade.**
 - 14/07/2023 - Added Dev Assistant CLI v0.2.46, featuring file management, Git version control, and terminal commands execution.
 - 14/07/2023 - "Test commit for pre-commit hook."
 - 14/07/2023 - Added Dev Assistant CLI and initial documentation.
 - 14/07/2023 - Data: 14/07/2023
 - 14/07/2023 - Added support for auto-deployment to PyPi using GitHub Actions.
 - 14/07/2023 - Dev Assistant CLI: Minor bug fixes and improvements.
 - 13/07/2023 - Fixed CLI terminal commands execution and added tests for 'cd' function.
 - 13/07/2023 - Updated tests and addressed issues in the codebase.

- Fixed an issue in the Git module (`dev_assistant_client/modules/git.py`).
- Resolved issue 4 (`issues/issue4.md`).
- Fixed issue 8 (`issues/issue8.md`).
- Added and updated tests in the test suite (`tests/test_git.py`).

A total of 46 insertions and 7 deletions were made in 4 files.
 - 13/07/2023 - Added support for Git version control commands, including initializing a Git repository, adding changes to the staging area, committing changes, and pushing changes to a remote repository.
 - 13/07/2023 - Implemented issue 5 and added tests (ba1955a)
 - 13/07/2023 - Added support for file management, terminal commands execution, and Git version control; refactored code and added tests.
 - 13/07/2023 - Data: 13/07/2023
 - 13/07/2023 - Added support for LLM instructions, refactored modules, and updated documentation (#123)
 - 13/07/2023 - **Atualização do Dev Assistant CLI:**

- O bug de codificação no módulo `file_management` foi corrigido.
 - 12/07/2023 - Fixed Dev Assistant CLI refactoring and added conditional encoding/decoding for improved security and performance.
 - 12/07/2023 - Data: 12/07/2023
 - 12/07/2023 - Fixed Dev Assistant CLI to handle file management, Git version control, and terminal commands execution.
 - 10/07/2023 - Fixed instruction flow in Dev Assistant CLI.


## Versão v0.1.3
 - 08/07/2023 - v0.1.3: Added file management, Git version control, and terminal commands execution features to Dev Assistant CLI.


## Versão v0.1.0
 - 05/07/2023 - Added support for file management, terminal commands execution, and Git version control; updated CLI presentation; and improved overall stability and usability.
 - 02/07/2023 - **Nova versão do Dev Assistant CLI disponível!**

A nova versão do Dev Assistant CLI inclui suporte para receber mensagens do Pusher, o que o torna mais estável e útil para os usuários.
 - 30/06/2023 - Updated setup.py and CHANGELOG.md for new version
 - 30/06/2023 - This update includes several changes to the Dev Assistant project, including an upgrade of the Python package and various alterations to the changelog. Here's a summary of the changes:

- `.env.example`: Added a single line to define a new environment variable.
- `README.md`: Added a section about contributing to the project.
- `dev_assistant_client/auth.py`: Made significant changes to the file, adding 76 lines.
- `dev_assistant_client/device.py`: Added 83 lines to the file.
- `dev_assistant_client/main.py`: Modified the file extensively, adding 109 lines and removing 90 lines.
- `dev_assistant_client/utils.py`: Added 15 lines to the file.
- `requirements.txt`: Made minor changes, adding 2 lines.
- `setup.py`: Made minor changes, adding 3 lines and removing 1 line.

These updates involve changes to various parts of the Dev Assistant project, such as authentication, device handling, and the main application. Additionally, the project now includes a section on contributing to the project.
 - 27/06/2023 - Added support for Dev Assistant CLI, featuring file management, Git version control, and terminal command execution.
 - 27/06/2023 - **Atualização do Dev Assistant CLI**

O commit 7e7de7233e93ecaf826d14f07ac4ccb01ac61256 removeu arquivos ignorados do repositório.
 - 27/06/2023 - Fixed Gitignore and updated documentation for Dev Assistant CLI.
 - 26/06/2023 - Initial commit of the Dev Assistant Local Client.
