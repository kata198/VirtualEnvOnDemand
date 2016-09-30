#!/usr/bin/env python
'''
    persistent_venv - An example that shows how to create and manage a persistent virtualenv environment at deploy-time.

        It is recommended that you put similar code into a "virtualenv.py" which you import from your executable, module, whatever.
'''


import os
import tempfile
import sys

from VirtualEnvOnDemand import createEnv, setGlobalVirtualEnv, getInfoFromVirtualEnv, activateEnv, installPackages

# Global pointer to the persistent virtualenv
global virtualenvInfo
virtualenvInfo = None

# Set to True to print what is going on, otherwise False
DEBUG = True


def _do_setup():
    '''
        _do_setup - Do the setup
    '''
    global virtualenvInfo, DEBUG
    PARENT_DIR = tempfile.gettempdir()

    VENV_NAME = 'TestEnv'

    VENV_PATH = os.sep.join([PARENT_DIR, VENV_NAME])

    PACKAGE_LIST = ['IndexedRedis', 'SimpleHttpFetch', 'AdvancedHTMLParser', 'cachebust==1.1.0']

    # Set the following to "True" if you update packages within PACKAGE_LIST, to trigger an install/upgrade of any new or updated packages.
    DO_INSTALL_PACKAGES = False

    if not os.path.isdir(VENV_PATH):
        if DEBUG:
            print ( "Creating Env...")
        virtualenvInfo = createEnv(packages=PACKAGE_LIST, parentDirectory=PARENT_DIR, name=VENV_NAME, stdout=None, stderr=None, deleteOnClose=False)
    else:
        if DEBUG:
            print ( "Using existing Env....")
        try:
            virtualenvInfo = getInfoFromVirtualEnv(VENV_PATH, validate=True)
        except ValueError as validationError:
            if DEBUG:
                print ( "Cannot use virtualenv, recreating. Reason: " + str(validationError) )
            virtualenvInfo = createEnv(packages=PACKAGE_LIST, parentDirectory=PARENT_DIR, name=VENV_NAME, stdout=None, stderr=None, deleteOnClose=False)

    # Use "activateEnv" to just activate this env as-is
    activateEnv(virtualenvInfo)

    if DO_INSTALL_PACKAGES:
        installPackages(PACKAGE_LIST, virtualenvInfo)

    ## use setGlobalVirtualEnv to use env as the global env, i.e. try to install packages upon failed imports

    #setGlobalVirtualEnv(virtualenvInfo, enableOnDemandImporter=True)

    

_do_setup()



# The following imports are not available without external installation
import SimpleHttpFetch
from AdvancedHTMLParser.exceptions import *




if __name__ == '__main__':
    sys.stdout.write('SimpleHttpFetch version: ' + SimpleHttpFetch.__version__ + '\n')
    import AdvancedHTMLParser
    sys.stdout.write('AdvancedHTMLParser version: ' + AdvancedHTMLParser.__version__ + '\n')

