# Copyright (c) 2015 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
#
#  VirtualEnvOnDemand provides a simple means for an application, without restarting, to temporarily install and use its runtime requirements  

# vim: ts=4 sw=4 expandtab

import atexit
import shutil
import sys
import tempfile
import subprocess
import virtualenv

from .exceptions import PipInstallFailed

__all__ = ('createEnv', '__version__', '__version_tuple__', 'PipInstallFailed')

__version__ = '1.0.0'
__version_tuple__ = (1, 0, 0)

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

            @return - On success, returns the following dict:
                {
                    'virtualenvDirectory'   : Absolute path to the root virtualenv directory
                    'sitePackagesDirectory' : Absolute path to the site-packages directory within
                    'requirements.txt'      : Full generated requirements.txt file used for pip installation
                }

        @raises - 
            VirtualEnvOnDemand.exceptions.PipInstallFailed -  if cannot install packages
            Others (Exception, etc)                        -  If permissions problem to write to specified directory, etc
    '''

    # Assemble the requirements for this env
    if not packages:
        reqContents = None
    else:
        if isinstance(packages, (list, tuple, set)):
            reqContents = '\n'.join(packages)
        elif isinstance(packages, dict):
            reqContents = []
            for name, value in packages.items():
                if not name:
                    raise ValueError('Missing name in packages dictionary.')
                if value:
                    reqContents.append("%s==%s" %(str(name), str(value)))
                else:
                    reqContents.append("%s" %(str(name),))
            reqContents = '\n'.join(reqContents)
        else:
            reqContents = packages

    # Create blank env
    venvDir = tempfile.mkdtemp(prefix='venv_', dir=parentDirectory)
    virtualenv.create_environment(venvDir, site_packages=True)

    # If they provided required packages (why wouldn't they?), install them
    if reqContents:
        with tempfile.NamedTemporaryFile(prefix='venv_req_', suffix='txt', mode='wt', dir=parentDirectory, delete=True) as reqFile:
            reqFile.write(reqContents)
            if reqContents[-1] != '\n':
                reqFile.write('\n')
            reqFile.flush()
            
            # If they chose to ignore output to one or more streams, setup a /dev/null stream
            devnull = None
            if stdout is None or stderr is None:
                devnull = open('/dev/null', 'wt')
                if stdout is None:
                    stdout = devnull
                if stderr is None:
                    stderr = devnull

            # Install from generated requirements.txt
            pipe = subprocess.Popen([venvDir + '/bin/pip', 'install', '-r', reqFile.name], shell=False, stdout=stdout, stderr=stderr)
            returnCode = pipe.wait()

            # Cleanup devnull stream if setup
            if devnull is not None:
                devnull.close()

            if returnCode != 0:
                raise PipInstallFailed(returnCode, reqContents)

    # Generate the site-packages path
    versionInfo = sys.version_info
    venvSitePath = "%s/lib/python%d.%d/site-packages" %(venvDir, versionInfo.major, versionInfo.minor)

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
    return {
        'virtualenvDirectory'   : venvDir,
        'sitePackagesDirectory' : venvSitePath,
        'requirements.txt'      : reqContents,
    }

def createEnvIfCannotImport(importName, packages, parentDirectory=None, stdout=sys.stdout, stderr=sys.stderr, deleteOnClose=True):
    '''
        createEnvIfCannotImport - Tries to import a given name, and if fails, creates a temporary env and installs given packages and tries again.

        @see createEnv for most params.

        @param importName - Name of module to import

        @raises - 
            VirtualEnvOnDemand.exceptions.PipInstallFailed -  if cannot install packages
            ImportError                                    -  if cannot import even after successful installation of the packages.
            Others (Exception, etc)                        -  If permissions problem to write to specified directory, etc

        @return - None if no env was created, otherwise the return dict from the createEnv call. @see createEnv
    '''
    ret = None

    try:
        __import__(importName)
    except ImportError:
        # Import failed, build our environment and try again.
        ret = createEnv(packages, parentDirectory, stdout, stderr, deleteOnClose)
        __import__(importName)

    return ret
        
