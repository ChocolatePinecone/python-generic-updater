# Python Visual Update Express

A dialog for updating an application by downloading files from a server. Designed to work like InstallForge's "Visual
Update Express".

This software may only be used as described in the LICENSE file. Please contact me through a github issue for questions
about commercial use.

Compatible with Python 3.10 and up

## Installation

```sh
python3 -m pip install python-visual-update-express
```

## Usage

### Add updater window in python

Import the UpdaterWindow and configure it

```python
from python_visual_update_express import UpdaterWindow

UPDATE_BASE_URL = 'https://yoursite.com/releases/yourapplication/'
CURRENT_VERSION = '1.0.1'
UPDATE_TARGET_DIR = 'C:/yourlocationpath'

updater_window = UpdaterWindow(UPDATE_BASE_URL, CURRENT_VERSION, UPDATE_TARGET_DIR)
```

Then when you are ready, simply call `show` on the window to start the updater:

```python
updater_window.show()
```

### Update script

The updater works according to an updatescript.ini file on the server.
This file tells the updater what versions of the application are supported and how to perform updates.
Make sure to have this file available on the server URL used by the updater.

This is a very simple example of an updatescript.ini:

```javascript
releases{
    1.0.0
    1.0.1
}

release:1.0.0{

}

release:1.0.1{
    DownloadFile:some-file.txt
}
```

#### Script commands

Currently only 1 command is available:

##### DownloadFile

This command will download a file on the speficied path, starting from the given update base URL + 'Updates/'.
So if for example the base URL of `https://yoursite.com/releases/yourapplication/` has been configured, a `DownloadFile:
dir1/some-file.txt` will download the file from
`https://yoursite.com/releases/yourapplication/Updates/dir1/some-file.txt`
