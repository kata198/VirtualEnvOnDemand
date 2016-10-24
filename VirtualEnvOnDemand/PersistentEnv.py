# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
'''
    PersistentEnv - "Helper" methods to manage a global persistent environment.

      For use in projects, deployments, etc.
'''

import os
import tempfile
import sys

from .CreateEnv import createEnv, activateEnv
from .GlobalEnv import setGlobalVirtualEnv
from .VirtualEnvInfo import getInfoFromVirtualEnv
from .InstallPackages import installPackages

from .utils import cmp_version, writeStrToFile


__all__ = ('setupAndActivateEnv', )

# Filename which marks "myVersion" on a virtualenv.
#  TODO: Maybe integrate this deeper into things, i.e. VirtualEnvInfo
MY_VERSION_FILENAME = '.VirtualEnvOnDemand_Version'

def setupAndActivateEnv(parentDirectory, name, packages, myVersion=None, forceInstallPackages=False, enableOnDemandImporter=False, printDebug=False):
    '''
        setupAndActivateEnv - 

            @param parentDirectory <str> - This is the directory wherein the virtualenv will be created
            @param name <str> - This is the name of the virtualenv root folder
            @param packages <list/dict/str> - A list of packages to install. You can use pip modifiers, like '==' and '<'. May be any of the following:

                List   - A list/tuple/set of package names (optionally including version requirements, e.x. MyPkg==1.2.3)
                Dict   - A dictionary of package names to versions. If no value is present (i.e. evaluates to False, like '' or None), the latest will be fetched.
                String - Directly becomes contents of requirements.txt file to be ingested by pip

    '''

    virtualenvInfo = None
    parentDirectory = tempfile.gettempdir()

    # venvPath - The combination of parentDirectory and name
    venvPath = os.sep.join([parentDirectory, name])

    # versionFilePath - The path to the file within the virtualenv root specifying a user-provided version.
    versionFilePath = os.sep.join([venvPath, MY_VERSION_FILENAME])

    doInstallPackages = bool(forceInstallPackages)
    if not doInstallPackages and myVersion:
        # could check if exists and not isfile here, but let's not add overhead for something stupid...
        if os.path.exists(versionFilePath):
            if not os.access(versionFilePath, os.R_OK):
                if printDebug is True:
                    sys.stderr.write ( 'VirtualEnvOnDemand: Access denied reading version file: "%s" , skipping version check.\n' %(versionFilePath,))
            else:
                currentVersion = None
                try:
                    with open(versionFilePath, 'rt') as f:
                        currentVersion = f.read().strip()
                except Exception as versionReadException:
                    if printDebug is True:
                        sys.stderr.write ( 'VirtualEnvOnDemand: Got exception reading from version file "%s": %s. Skipping version check.\n' %(versionFilePath, str(versionReadException)) )

                if not currentVersion or cmp_version(currentVersion, myVersion) == -1:
                    doInstallPackages = True
        else:
            # No previous version, we will set it.
            doInstallPackages = True

    # If there is no folder where our virtualenv should be, we must create it.
    if not os.path.isdir(venvPath):
        if printDebug:
            sys.stderr.write ( "Creating Env...\n")
        virtualenvInfo = createEnv(packages=packages, parentDirectory=parentDirectory, name=name, stdout=None, stderr=None, deleteOnClose=False)
        _writeVersionFileContents(versionFilePath, myVersion, printDebug)

        doInstallPackages = False
    else:
        # Otherwise, validate that there is a virtualenv here, and that it is usable (validate).
        if printDebug:
            sys.stderr.write ( "Using existing Env....\n")
        try:
            virtualenvInfo = getInfoFromVirtualEnv(venvPath, validate=True)
        except ValueError as validationError:
            # This virtualenv is not usable. Maybe it is an empty directory, maybe something else. validationError will have the given reason.
            #  so create a virtualenv at this location.
            if printDebug:
                sys.stderr.write ( "Cannot use virtualenv, recreating. Reason: " + str(validationError) + "\n" )
            virtualenvInfo = createEnv(packages=packages, parentDirectory=parentDirectory, name=name, stdout=None, stderr=None, deleteOnClose=False)
            _writeVersionFileContents(versionFilePath, myVersion, printDebug)

            doInstallPackages = False

    # If this flag is set, try to update packages, and install any new ones.
    if doInstallPackages:
        if printDebug:
            (useStdout, useStderr) = (sys.stderr, sys.stderr)
        else:
            (useStdout, useStderr) = (None, None)
        installPackages(packages, virtualenvInfo, stdout=useStdout, stderr=useStderr)
        _writeVersionFileContents(versionFilePath, myVersion, printDebug)

    # Use "activateEnv" to just activate this env as-is
    activateEnv(virtualenvInfo)

    if enableOnDemandImporter:
        setGlobalVirtualEnv(virtualenvInfo, enableOnDemandImporter=True)

    return virtualenvInfo


def _writeVersionFileContents(filename, myVersion, printDebug=False):
    if myVersion in (None, False):
        return

    myVersion = str(myVersion)
    ex = writeStrToFile(filename, myVersion)
    if ex and printDebug is True:
        sys.stderr.write('Failed to update file "%s" with user-provided version "%s". Error was: %s\n' %(filename, myVersion, str(ex)))
    return ex
        
