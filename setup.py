from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='dev-assistant-client',
    version='0.1.32',
    url='https://github.com/lucianotonet/dev-assistant-client',
    author='Luciano Tonet',
    author_email='tonetlds@gmail.com',
    description='A local extension for ChatGPT plugin DevAssistant, which helps you with your development tasks straight in your machine.',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'dev-assistant=devassistant.main:run',
            'devassistant=devassistant.main:run',
            'dev-assistant-client=devassistant.main:run',
        ],
    },
)