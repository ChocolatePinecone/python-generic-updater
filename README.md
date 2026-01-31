# Python Visual Update Express

A dialog for updating an application by downloading files from a server. Designed to work like InstallForge's "Visual
Update Express".

## Development Commands

### Setup

First create a new python virtual environment. this will create a virtual environment in the 'venv' directory

```sh
python -m venv venv
source venv/bin/activate # This activates the virtual environment
```

Or in Windows PowerShell:

```sh
py -m venv venv
.\venv\Scripts\activate # This activates the virtual environment
```

To set up all required dependencies, run pip with the requirements.txt:

```sh
python -m pip install -r requirements.txt
```

### Build application

For releasing a new build on PyPi, follow these steps:

- First, Update the release version in the pyproject.toml

- Build the python package files with the command

```sh
python -m build
```

- Upload the new release to PyPi

```sh
python -m twine upload --repository pypi dist/*
```
