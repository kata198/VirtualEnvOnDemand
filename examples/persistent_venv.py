#!/usr/bin/env python

import os
import tempfile
import sys

from VirtualEnvOnDemand import createEnv, setGlobalVirtualEnv, getInfoFromVirtualEnv, activateEnv

PARENT_DIR = tempfile.gettempdir()

VENV_NAME = 'TestEnv'

VENV_PATH = os.sep.join([PARENT_DIR, VENV_NAME])

PACKAGE_LIST = ['IndexedRedis', ]

if not os.path.isdir(VENV_PATH):
    print ( "Creating Env...")
    virtualenvInfo = createEnv(packages=PACKAGE_LIST, parentDirectory=PARENT_DIR, name=VENV_NAME, deleteOnClose=False)
else:
    print ( "Using existing Env....")
    try:
        virtualenvInfo = getInfoFromVirtualEnv(VENV_PATH, validate=True)
    except ValueError:
        print ( "Cannot use virtualenv, recreating" )
        virtualenvInfo = createEnv(packages=PACKAGE_LIST, parentDirectory=PARENT_DIR, name=VENV_NAME, deleteOnClose=False)

# Use "activateEnv" to just activate this env as-is
activateEnv(virtualenvInfo)

## use setGlobalVirtualEnv to use env as the global env, i.e. try to install packages upon failed imports

#setGlobalVirtualEnv(virtualenvInfo, enableOnDemandImporter=True)

# The following imports are not available without external installation
import SimpleHttpFetch
from AdvancedHTMLParser.exceptions import *




if __name__ == '__main__':
    sys.stdout.write('SimpleHttpFetch version: ' + SimpleHttpFetch.__version__ + '\n')
    import AdvancedHTMLParser
    sys.stdout.write('AdvancedHTMLParser version: ' + AdvancedHTMLParser.__version__ + '\n')

