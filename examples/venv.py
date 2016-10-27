#!/usr/bin/env python
'''
    persistent_venv_old - An example that shows how to create and manage a persistent virtualenv environment at deploy-time.

    NOTE: THIS IS THE OLD METHOD, you will likely want to use the more simple "setupAndActivateEnv" for your project.
    
        It is recommended that you put similar code into a "myenv.py" which you import from your executable, module, whatever.
'''


import os
import tempfile
import sys

from VirtualEnvOnDemand import setupAndActivateEnv

# PARENT_DIR - This is the directory wherein the virtualenv will be created
PARENT_DIR = tempfile.gettempdir()

# VENV_NAME - This is the name of the virtualenv root folder
VENV_NAME = 'TestEnv'

# VENV_VERSION - This is the "version" of your virtualenv. When you update your package list, you will 
#   want to bump this so that VirtualEnvOnDemand checks for and installs updates.
VENV_VERSION = '1.0'

# PACKAGE_LIST - A list of packages to install. You can use pip modifiers, like '==' and '<'
PACKAGE_LIST = ['IndexedRedis', 'SimpleHttpFetch', 'AdvancedHTMLParser', 'cachebust==1.1.0']

# Global pointer to the persistent virtualenv
virtualenvInfo = setupAndActivateEnv(PARENT_DIR, VENV_NAME, PACKAGE_LIST, VENV_VERSION, 
    forceInstallPackages=False, enableOnDemandImporter=False, printDebug=False)
