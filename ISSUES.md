# Issues

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