import os
import subprocess
import toml
import requests
import logging
from packaging import version
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def get_local_version():
    logging.info("Retrieving local version...")
    pyproject_file_path = Path('pyproject.toml').resolve()
    with open(pyproject_file_path, 'r') as file:
        pyproject_data = toml.load(file)
    logging.info("Local version retrieved.")
    return pyproject_data['tool']['poetry']['version']

def get_online_version():
    logging.info("Retrieving online version...")
    response = requests.get(f"https://pypi.org/pypi/dev-assistant-client/json")
    logging.info("Online version retrieved.")
    return response.json()["info"]["version"]

def get_latest_git_tag():
    logging.info("Retrieving the latest git tag...")
    latest_tag = subprocess.getoutput("git describe --tags --abbrev=0")
    logging.info("Latest git tag retrieved.")
    return latest_tag.replace('v', '')

def bump_version(local_version, online_version, git_tag_version):
    logging.info("Checking versions...")
    max_version = max(version.parse(local_version), version.parse(online_version), version.parse(git_tag_version))
    logging.info("Incrementing the version...")
    version_parts = str(max_version).split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = '.'.join(version_parts)
    logging.info("New version generated.")
    return new_version

def update_pyproject_file(new_version):
    logging.info("Updating the pyproject.toml file...")
    pyproject_file_path = Path('pyproject.toml').resolve()
    with open(pyproject_file_path, 'r') as file:
        pyproject_data = toml.load(file)
    pyproject_data['tool']['poetry']['version'] = new_version
    with open(pyproject_file_path, 'w') as file:
        toml.dump(pyproject_data, file)
    logging.info("pyproject.toml file updated.")

def git_commit_and_tag(new_version):
    logging.info("Committing new version and creating git tag...")
    try:
        subprocess.run(["git", "config", "user.name", "Dev Assistant AI"], check=True)
        subprocess.run(["git", "config", "user.email", "devassistant@tonet.dev"], check=True)
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"], check=True)
        subprocess.run(["git", "tag", f"v{new_version}"], check=True)
        subprocess.run(["git", "push", "origin", "--tags"], check=True)
        logging.info("Git commit and tag created and pushed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while committing and tagging: {e}")
    subprocess.run(f"echo ::set-output name=tag::v{new_version}", shell=True, check=True)
        
if __name__ == "__main__":
    logging.info("Starting the version update process...")
    local_version = get_local_version()
    online_version = get_online_version()
    git_tag_version = get_latest_git_tag()
    new_version = bump_version(local_version, online_version, git_tag_version)
    update_pyproject_file(new_version)
    git_commit_and_tag(new_version)
    logging.info("Version update process completed.")
