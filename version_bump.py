import subprocess
import toml
from pathlib import Path
import logging
from packaging import version

logging.basicConfig(level=logging.INFO)

def get_local_version() -> str:
    with open('pyproject.toml', 'r') as file:
        data = toml.load(file)
    return data['tool']['poetry']['version']

def get_latest_git_tag() -> str:
    try:
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], text=True).strip()
    except subprocess.CalledProcessError:
        tag = 'v0.0.0'
    return tag.lstrip('v')

def increment_version(ver: str) -> str:
    v = version.parse(ver)
    if isinstance(v, version.Version):
        return f"{v.major}.{v.minor}.{v.micro + 1}" # Incrementa o micro
    else:
        return '0.0.1'

def tag_exists(tag: str) -> bool:
    try:
        subprocess.check_output(['git', 'rev-parse', f'v{tag}'], text=True)
        return True
    except subprocess.CalledProcessError:
        return False

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
        # Check if the tag exists and increment version if necessary
        while tag_exists(new_version):
            logging.info(f"Tag v{new_version} already exists. Incrementing version...")
            new_version = increment_version(new_version)
            update_pyproject_file(new_version)
        subprocess.run(["git", "tag", f"v{new_version}"], check=True)
        subprocess.run(["git", "push", "origin", "HEAD", "--tags"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while committing and tagging: {e}")
    finally:
        subprocess.run(f"echo ::set-output name=tag::v{new_version}", shell=True, check=True)

if __name__ == "__main__":
    logging.info("Starting the version update process...")
    local_version = get_local_version()
    git_tag_version = get_latest_git_tag()
    new_version = increment_version(max(local_version, git_tag_version, key=version.parse))
    update_pyproject_file(new_version)
    git_commit_and_tag(new_version)
    logging.info("Version update process completed.")