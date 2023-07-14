# Issue 2

## Issue Description

We are facing an issue with the 'cd' command in the Dev Assistant client. The issue is that the current directory is being reset to the original directory after the execution of the 'cd' command. This suggests that the update of the terminal state is not working as expected.

The expected behavior is that the 'cd' command changes the current directory and the new directory persists for the subsequent commands. However, what we are observing is that the current directory is being reset to the original directory after the execution of the 'cd' command.

We have tried several approaches to solve this issue, including trying to update the terminal state after the execution of the 'cd' command and running each command in a new shell process that starts in the desired directory. However, none of these approaches have solved the issue.

This issue is critical for the functionality of the Dev Assistant client as it prevents the execution of commands in the desired directory. This can affect the ability of the client to perform tasks such as reading and writing files in specific directories.

We need to investigate this issue further to understand what is causing it and how it can be resolved. This may involve adding more logs to the code to track the execution flow, checking the environment in which the code is being run to ensure it supports changing the directory, and checking for any configuration or restriction in the environment that is preventing the change of directory.

