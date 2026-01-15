# Python generic updater

A dialog for updating specific files by syncing them to a server. Designed to work like InstallForge's "Visual Update Express".

This software may only be used as described in the LICENSE file. Please contact me through a github issue for questions about commercial use.

Compatible with Python 3.10 and up

## Installation
TODO: Insert instructions, hopefully just downloading this as a package with pip??

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

For windows:

```sh
pyinstaller -n "app-name" --noconsole --add-binary="libs/*;." --onefile updater.py
```

More information about using pyinstaller: https://www.pythonguis.com/tutorials/packaging-pyqt6-applications-windows-pyinstaller/

### Usage
TODO: Add explanation about setting up an updatescript.ini like below:

```javascript
releases{
    1.0.0
    1.0.1 // Add the new version like this. Keep previous version in the list, otherwise those versions cannot update.
}

release:1.0.0{

}

release:1.0.1{
    DownloadFile:filename
}
```