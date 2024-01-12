import subprocess
import toml
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def get_local_version() -> str:
    with open('pyproject.toml', 'r') as file:
        data = toml.load(file)
    return data['tool']['poetry']['version']

def get_online_version() -> str:
    # Placeholder function to get the latest version from an online source
    return '0.0.0'

def get_latest_git_tag() -> str:
    try:
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], text=True).strip()
    except subprocess.CalledProcessError:
        tag = 'v0.0.0'
    return tag.lstrip('v')

def increment_version(local: str, online: str, git_tag: str) -> str:
    # Increment the version number based on the specific versioning scheme
    return max(local, online, git_tag, key=lambda v: [int(x) for x in v.split('.')])

def update_file_version(file_path: Path, new_version: str):
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
                new_version = increment_version(new_version, '0.0.0', '0.0.0')
        subprocess.run(["git", "push", "origin", "HEAD", "--tags"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        subprocess.run(f"echo ::set-output name=tag::v{new_version}", shell=True, check=True)
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

