import os
from setuptools import setup 

APP = ['main.py']
APP_NAME = 'FTP Client Program'
DATA_FILES = [
    os.path.join(os.path.dirname(__file__), 'icons/delete.png'),
    os.path.join(os.path.dirname(__file__), 'icons/directory.png'),
    os.path.join(os.path.dirname(__file__), 'icons/error.png'),
    os.path.join(os.path.dirname(__file__), 'icons/file.png'),
    os.path.join(os.path.dirname(__file__), 'icons/left.png'),
    os.path.join(os.path.dirname(__file__), 'icons/loadingSpinner.png'),
    os.path.join(os.path.dirname(__file__), 'icons/right.png')
    # add icon files 
]

OPTIONS = {
    'argv_emulation': True, # provides emulator for `open application` and `open document` events 
    'includes': ['sip', 'PyQt5'] # used for including extra Python modules that didn't get automatically included 
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    setup_requires=['py2app'],
)