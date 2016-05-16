# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"

# vim: ts=4 sw=4 expandtab

import os
import atexit
import shutil
import sys
import tempfile
import virtualenv

from .VirtualEnvInfo import VirtualEnvInfo
from .InstallPackages import installPackages

__all__ = ('createEnv', 'createEnvIfCannotImport')

def createEnv(packages, parentDirectory=None, stdout=sys.stdout, stderr=sys.stderr, deleteOnClose=True):
    '''
        createEnv - Creates a temporary virtual environment and installs the required modules for the current running application.
            You can use this, for example, to "recover" from a failed import by installing the software on demand.

            @param packages - Describes the required packages. Takes one of the following forms:

                String - Directly becomes contents of requirements.txt file to be ingested by pip
                List   - A list/tuple/set of package names (optionally including version requirements, e.x. MyPkg==1.2.3)
                Dict   - A dictionary of package names to versions. If no value is present, the latest will be fetched.

            @param parentDirectory <str> - Parent directory of the directory which will be created to hold the temporary environment and packages. Defaults to tempfile.tempdir
            @param stdout <iostream/None> - Stream to be used as stdout for installation. Default is sys.stdout. Use "None" to swallow output.
            @param stderr <iostream/None> - Stream to be used as stderr for installation. Default is sys.stderr. Use "None" to swallow output.

            @param deleteOnClose <bool> - If True (Default), this temporary environment and packages will be erased after program terminates. Note, this cannot trap everything (e.x. SIGKILL).

            @return - On success, returns a VirtualEnvInfo object, which can be used as a dict with the following fields:
                {
                    'virtualenvDirectory'   : Absolute path to the root virtualenv directory
                    'sitePackagesDirectory' : Absolute path to the site-packages directory within
                    'requirements.txt'      : Full generated requirements.txt file used for pip installation
                }

        @raises - 
            VirtualEnvOnDemand.exceptions.PipInstallFailed -  if cannot install packages
            Others (Exception, etc)                        -  If permissions problem to write to specified directory, etc
    '''
    # Create blank env
    venvDir = tempfile.mkdtemp(prefix='venv_', dir=parentDirectory)
    virtualenv.create_environment(venvDir, site_packages=True)

    # If they provided required packages, install them
    reqContents = installPackages(packages, venvDir, stdout, stderr)

    # Generate the site-packages path
    versionInfo = sys.version_info
    venvSitePath = os.sep.join([venvDir, 'lib', "python%d.%d" %(versionInfo.major, versionInfo.minor), "site-packages"])

    # If we are to delete this env upon the app closing, 
    if deleteOnClose is True:
        def _cleanupFunc():
            # Remove from path
            try:
                sys.path.remove(venvSitePath)
            except:
                pass

            # Remove physical directory
            try:
                shutil.rmtree(venvDir)
            except:
                pass

        atexit.register(_cleanupFunc)

    # Actually append the new site-packages dir to the runtime path so people can start importing!
    sys.path = [venvSitePath] + sys.path

    # aaannnd return some meta information.
    return VirtualEnvInfo(
        virtualenvDirectory=venvDir,
        sitePackagesDirectory=venvSitePath,
        requirementsTxt=reqContents,
    )

def createEnvIfCannotImport(importName, packages, parentDirectory=None, stdout=sys.stdout, stderr=sys.stderr, deleteOnClose=True):
    '''
        createEnvIfCannotImport - Tries to import a given name, and if fails, creates a temporary env and installs given packages and tries again.

        @see createEnv for most params.

        @param importName - Name of module to import

        @raises - 
            VirtualEnvOnDemand.exceptions.PipInstallFailed -  if cannot install packages
            ImportError                                    -  if cannot import even after successful installation of the packages.
            Others (Exception, etc)                        -  If permissions problem to write to specified directory, etc

        @return - None if no env was created, otherwise the return VirtualEnvInfo object from the createEnv call. @see createEnv
    '''
    ret = None

    try:
        __import__(importName)
    except ImportError:
        # Import failed, build our environment and try again.
        ret = createEnv(packages, parentDirectory, stdout, stderr, deleteOnClose)
        __import__(importName)

    return ret

