import os
import re
import subprocess
import toml
import requests
import logging
from packaging import version
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def retrieve_version(file_path: Path, key: str) -> str:
    logging.info(f"Retrieving {key} version...")
    with open(file_path, 'r') as file:
        data = toml.load(file)
    logging.info(f"{key} version retrieved.")
    return data['tool']['poetry']['version']

def get_local_version() -> str:
    return retrieve_version(Path('pyproject.toml').resolve(), "local")

def get_online_version() -> str:
    logging.info("Retrieving online version...")
    response = requests.get(f"https://pypi.org/pypi/dev-assistant-client/json")
    logging.info("Online version retrieved.")
    return response.json()["info"]["version"]

def get_latest_git_tag() -> str:
    logging.info("Retrieving the latest git tag...")
    latest_tag = subprocess.getoutput("git describe --tags --abbrev=0")
    logging.info("Latest git tag retrieved.")
    cleaned_tag = re.sub(r'[^0-9\.]', '', latest_tag)
    if not cleaned_tag or not cleaned_tag[0].isdigit():
        raise ValueError(f"Invalid tag format: {latest_tag}")
    return str(version.parse(cleaned_tag))

def increment_version(*versions: str) -> str:
    logging.info("Checking versions...")
    max_version = max(version.parse(v) for v in versions)
    logging.info("Incrementing the version...")
    version_parts = str(max_version).split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = '.'.join(version_parts)
    logging.info("New version generated.")
    return new_version

def update_file_version(file_path: Path, new_version: str):
    logging.info("Updating the file version...")
    with open(file_path, 'r') as file:
        data = toml.load(file)
    data['tool']['poetry']['version'] = new_version
    with open(file_path, 'w') as file:
        toml.dump(data, file)
    logging.info("File version updated.")

def update_pyproject_file(new_version: str):
    update_file_version(Path('pyproject.toml').resolve(), new_version)

def git_commit_and_tag(new_version: str):
    logging.info("Committing new version and creating git tag...")
    try:
        subprocess.run(["git", "config", "user.name", "Dev Assistant AI"], check=True)
        subprocess.run(["git", "config", "user.email", "devassistant@tonet.dev"], check=True)
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"], check=True)
        while True:
            try:
                subprocess.run(["git", "tag", f"v{new_version}"], check=True)
                break
            except subprocess.CalledProcessError:
                logging.info("Tag already exists, incrementing the version...")
                new_version = increment_version(new_version)
                update_pyproject_file(new_version)
        subprocess.run(["git", "push", "origin", "--tags"], check=True)
        subprocess.run(f"echo ::set-output name=tag::v{new_version}", shell=True, check=True)
        logging.info("Git commit and tag created and pushed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while committing and tagging: {e}")
        
if __name__ == "__main__":
    logging.info("Starting the version update process...")
    local_version = get_local_version()
    online_version = get_online_version()
    git_tag_version = get_latest_git_tag()
    new_version = increment_version(local_version, online_version, git_tag_version)
    update_pyproject_file(new_version)
    git_commit_and_tag(new_version)
    logging.info("Version update process completed.")
