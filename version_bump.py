import os
import subprocess
import toml
import requests
from packaging import version
from pathlib import Path

def get_local_version():
    print("Retrieving local version...")
    pyproject_file_path = Path('pyproject.toml').resolve()
    with open(pyproject_file_path, 'r') as file:
        pyproject_data = toml.load(file)
    print("Local version retrieved.")
    return pyproject_data['tool']['poetry']['version']

def get_online_version():
    print("Retrieving online version...")
    response = requests.get(f"https://pypi.org/pypi/dev-assistant-client/json")
    print("Online version retrieved.")
    return response.json()["info"]["version"]

def bump_version(local_version, online_version):
    print("Checking if the online version is greater than the local version...")
    if version.parse(online_version) > version.parse(local_version):
        print("The online version is greater. Incrementing the version...")
        version_parts = online_version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = '.'.join(version_parts)
        print("New version generated.")
        return new_version
    elif version.parse(online_version) == version.parse(local_version):
        print("The versions are equal. Incrementing the version...")
        version_parts = local_version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = '.'.join(version_parts)
        print("New version generated.")
        return new_version
    print("The local version is greater. Keeping the same version.")
    return local_version

def update_pyproject_file(new_version):
    print("Updating the pyproject.toml file...")
    pyproject_file_path = Path('pyproject.toml').resolve()
    with open(pyproject_file_path, 'r') as file:
        pyproject_data = toml.load(file)
    pyproject_data['tool']['poetry']['version'] = new_version
    with open(pyproject_file_path, 'w') as file:
        toml.dump(pyproject_data, file)
    print("pyproject.toml file updated.")

def git_commit_and_tag(new_version):
    print("Committing new version and creating git tag...")
    try:
        subprocess.run(["git", "config", "user.name", "Dev Assistant AI"], check=True)
        subprocess.run(["git", "config", "user.email", "devassistant@tonet.dev"], check=True)
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"], check=True)
        subprocess.run(["git", "tag", f"v{new_version}"], check=True)
        subprocess.run(["git", "push", "origin", "--tags"], check=True)
        print("Git commit and tag created and pushed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while committing and tagging: {e}")
    subprocess.run(f"echo ::set-output name=tag::v${new_version}", shell=True, check=True)
        
if __name__ == "__main__":
    print("Starting the version update process...")
    local_version = get_local_version()
    online_version = get_online_version()
    new_version = bump_version(local_version, online_version)
    if new_version != local_version:
        update_pyproject_file(new_version)
        git_commit_and_tag(new_version)
    print("Version update process completed.")
