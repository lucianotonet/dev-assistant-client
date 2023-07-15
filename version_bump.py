import re

with open('setup.py', 'r') as file:
    setup_file = file.read()

version = re.search(r"version='(.*?)'", setup_file).group(1)
version_parts = version.split('.')
version_parts[-1] = str(int(version_parts[-1]) + 1)
new_version = '.'.join(version_parts)

setup_file = re.sub(r"version='(.*?)'", f"version='{new_version}'", setup_file)

with open('setup.py', 'w') as file:
    file.write(setup_file)