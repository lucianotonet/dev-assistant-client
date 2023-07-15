# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.7] - 2023-07-14

### Added

- Added Github Actions workflow for automatic deployment to PyPi. This workflow will automatically deploy the package to PyPi whenever changes are pushed to the main branch.
- Added pre-commit hook for automatic version bump. This hook will automatically increment the package version whenever a commit is made.

## [0.1.6] - 2023-07-14

### Fixed

- Fixed encoding issue in file_management module when creating and updating files. This fix ensures that files can be created and updated without encountering encoding issues.
