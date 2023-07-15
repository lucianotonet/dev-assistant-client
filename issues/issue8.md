# Issue 8

## Problem

We are experiencing an issue with reading the README.md file due to an encoding problem. The error message is: 'charmap' codec can't decode byte 0x8f in position 1040: character maps to <undefined>.

## Steps to Reproduce

1. Try to read the README.md file using the `files_read_file` operation.

## Expected Behavior

The README.md file should be read without any encoding issues.

## Actual Behavior

An encoding error occurs when trying to read the README.md file.