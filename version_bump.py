import toml
import requests
from packaging import version

def get_local_version():
    with open('pyproject.toml', 'r') as file:
        pyproject_file = file.read()
    pyproject_data = toml.loads(pyproject_file)
    return pyproject_data['tool']['poetry']['version']

def get_online_version():
    response = requests.get(f"https://pypi.org/pypi/dev-assistant-client/json")
    return response.json()["info"]["version"]

def bump_version(local_version, online_version):
    if version.parse(online_version) > version.parse(local_version):
        version_parts = online_version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = '.'.join(version_parts)
        return new_version
    return local_version

def update_pyproject_file(new_version):
    with open('pyproject.toml', 'r') as file:
        pyproject_data = toml.loads(file.read())
    pyproject_data['tool']['poetry']['version'] = new_version
    new_pyproject_file = toml.dumps(pyproject_data)
    with open('pyproject.toml', 'w') as file:
        file.write(new_pyproject_file)

local_version = get_local_version()
online_version = get_online_version()
new_version = bump_version(local_version, online_version)
update_pyproject_file(new_version)