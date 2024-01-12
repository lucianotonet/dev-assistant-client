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
        tags = subprocess.check_output(['git', 'tag'], text=True).strip().split('\n')
        # Filter out empty strings and sort in descending order
        tags = sorted(filter(None, tags), key=lambda t: version.parse(t.lstrip('v')), reverse=True)
        if tags:
            return tags[0].lstrip('v')
    except subprocess.CalledProcessError:
        pass
    return '0.0.0'

def increment_version(ver: str) -> str:
    v = version.parse(ver)
    if isinstance(v, version.Version):
        return f"{v.major}.{v.minor}.{v.micro + 1}"
    else:
        return '0.0.1'

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
        # Increment version until a unique tag is found
        while subprocess.run(["git", "tag", "-l", f"v{new_version}"], capture_output=True, text=True).stdout.strip():
            logging.info(f"Tag v{new_version} already exists. Incrementing version...")
            new_version = increment_version(new_version)
            update_pyproject_file(new_version)
        subprocess.run(["git", "tag", f"v{new_version}"], check=True)
        subprocess.run(["git", "push", "origin", "HEAD", "--tags"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while committing and tagging: {e}")
    finally:
        subprocess.run(["git", "push", "origin", "main"], check=True)
        # Use the new GitHub Actions set-output syntax
        print(f"::set-output name=tag::v{new_version}")

if __name__ == "__main__":
    logging.info("Starting the version update process...")
    local_version = get_local_version()
    git_tag_version = get_latest_git_tag()
    new_version = increment_version(max(local_version, git_tag_version, key=version.parse))
    update_pyproject_file(new_version)
    git_commit_and_tag(new_version)
    logging.info("Version update process completed.")