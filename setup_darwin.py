"""
py2app/py2exe build script for MyApplication.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
 python setup_win.py py2app

Usage (Windows):
 python setup_win.py py2exe
"""
from glob import glob

import sys
from setuptools import setup

mainscript = 'main.py'

DATA_FILES = ['config.txt',
              ('ui/images', glob('ui/images/*.png'))]

if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        data_files=DATA_FILES,
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        options=dict(py2app=dict(argv_emulation=True)),
    )
elif sys.platform == 'win32':
    import py2exe
    extra_options = dict(
        setup_requires=['py2exe'],
        app=[mainscript],
        data_files=DATA_FILES
    )
else:
    extra_options = dict(
        # Normally unix-like platforms will use "setup_darwin.py install"
        # and install the main script as such
        scripts=[mainscript],
    )

setup(
    name="The Blob",
    **extra_options
)
