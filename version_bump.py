import re
import toml

with open('pyproject.toml', 'r') as file:
    pyproject_file = file.read()

pyproject_data = toml.loads(pyproject_file)
version = pyproject_data['tool']['poetry']['version']
version_parts = version.split('.')
version_parts[-1] = str(int(version_parts[-1]) + 1)
new_version = '.'.join(version_parts)

pyproject_data['tool']['poetry']['version'] = new_version
new_pyproject_file = toml.dumps(pyproject_data)

with open('pyproject.toml', 'w') as file:
    file.write(new_pyproject_file)
