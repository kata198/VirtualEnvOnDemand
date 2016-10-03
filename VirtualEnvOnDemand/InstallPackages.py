# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
#
#  Package installation methods

import imp
import os
import tempfile
import subprocess
import sys

from .VirtualEnvInfo import VirtualEnvInfo
from .exceptions import PipInstallFailed, VirtualEnvDoesNotExist

__all__ = ('installPackages', 'ensureImport', 'generateRequirementsTxt')

def installPackages(packages, venvDir, stdout=sys.stdout, stderr=sys.stderr):
    '''
        installPackages - Installs packages into a created virtual environment

            @param packages - Describes the required packages. Takes one of the following forms:

                String - Directly becomes contents of requirements.txt file to be ingested by pip
                List   - A list/tuple/set of package names (optionally including version requirements, e.x. MyPkg==1.2.3)
                Dict   - A dictionary of package names to versions. If no value is present, the latest will be fetched.

            @param venvDir <str/VirtualEnvInfo> - Path to a created virtualenv directory. This should be the 'virtualenvDirectory' key from the return of createEnv, or just the VirtualEnvInfo object itself will work.
            @param stdout <iostream/None> - Stream to be used as stdout for installation. Default is sys.stdout. Use "None" to swallow output.
            @param stderr <iostream/None> - Stream to be used as stderr for installation. Default is sys.stderr. Use "None" to swallow output.

            @return - The generated requirements.txt used to install packages.

            @raises - 
                VirtualEnvOnDemand.exceptions.PipInstallFailed -  if cannot install packages
                VirtualEnvOnDemand.exceptions.VirtualEnvDoesNotExist - If given venvDir does not exist
                Others (Exception, etc)                        -  If permissions problem to write to specified directory, etc
    '''
    if isinstance(venvDir, VirtualEnvInfo):
        venvDir = venvDir['virtualenvDirectory']

    if not venvDir or not os.path.isdir(venvDir) or not os.path.isdir(venvDir + '/bin'):
        raise VirtualEnvDoesNotExist('Provided virtualenv directory "%s" is not present, is not a directory, or has not been setup.' %(str(venvDir),))

    # Get packages
    reqContents = generateRequirementsTxt(packages)

    if reqContents:
        # Generate a temporary named file for the requirements.txt and feed into pip
        with tempfile.NamedTemporaryFile(prefix='venv_req_', suffix='txt', mode='wt', dir=venvDir, delete=True) as reqFile:
            reqFile.write(reqContents)
            if reqContents[-1] != '\n':
                reqFile.write('\n')
            reqFile.flush()
            
            # If they chose to ignore output to one or more streams, setup a /dev/null stream
            devnull = None
            if stdout is None or stderr is None:
                devnull = open(os.devnull, 'wt')
                if stdout is None:
                    stdout = devnull
                if stderr is None:
                    stderr = devnull

            # Install from generated requirements.txt
            pipe = subprocess.Popen([ os.sep.join([venvDir, 'bin', 'pip']), 'install', '--upgrade', '-r', reqFile.name], shell=False, stdout=stdout, stderr=stderr)
            returnCode = pipe.wait()

            # Cleanup devnull stream if setup
            if devnull is not None:
                devnull.close()

            if returnCode != 0:
                raise PipInstallFailed(returnCode, reqContents)

    return reqContents

def ensureImport(importName, venvDir, packageName=None, stdout=None, stderr=None):
    '''
        ensureImport - Try to import a module, and upon failure to import try to install package into provided virtualenv

        @param importName <str> - The name of the module to import
        @param venvDir <str/VirtualEnvInfo> - The path to a virtualenv, likely created by createEnv or the global env (fetched via getGlobalVirtualEnvInfo()).
        @param packageName <str/None> - If the package name differs from the import name (like biopython package provides "Bio" module), install this package if import fails. This may contain version info (like AdvancedHTMLParser>6.0)
        @param stdout <stream/None> - Stream to use for stdout as package info, or None to silence. Default None. NOTE: This differs from elsewhere where sys.stdout is default.
        @param stderr <stream/None> - Stream to use for stderr as package info, or None to silence. Default None. NOTE: This differs from elsewhere where sys.stderr is default.

        @return - The imported module

        @raises - ImportError if cannot import.

            NOTE: With this method, PipInstallFailed will be intercepted and ImportError thrown instead, as this is intended to be a drop-in replacement for "import" when the package name differs.
    '''

    # Try first if in sys.modules
    if importName in sys.modules:
        return sys.modules[importName]

    # Next, try to resolve directly with "imp" so we don't go through our custom importer
    modInfo = None
    try:
        modInfo = imp.find_module(importName)
    except ImportError:
        pass
    if modInfo is not None:
        return imp.load_module(importName, *modInfo)

    # Module is not available, so try to install
    if not packageName:
        packageName = importName
    
    # Same logic already exists in installPackages
#    if isinstance(venvDir, VirtualEnvInfo):
#        venvDir = venvDir['virtualenvDirectory']
#
#    if not venvDir or not os.path.isdir(venvDir):
#        raise ValueError('Provided virtualenv directory "%s" is not present or not a directory.' %(str(venvDir),))

    installPackages(packageName, venvDir, stdout, stderr)
    
    modInfo = imp.find_module(importName)
    return imp.load_module(importName, *modInfo)


def generateRequirementsTxt(packages):
    '''
        generateRequirementsTxt - Generates a requirements.txt suitable for pip to ingest based on packages param.

            @param packages - Describes the required packages. Takes one of the following forms:

                String - Directly becomes contents of requirements.txt file to be ingested by pip
                List   - A list/tuple/set of package names (optionally including version requirements, e.x. MyPkg==1.2.3)
                Dict   - A dictionary of package names to versions. If no value is present, the latest will be fetched.

            @return <str> - generated requirements.txt file contents
    '''

    if not packages:
        reqContents = ''
    elif isinstance(packages, (list, tuple, set)):
        # A simple list potentially including qualifiers
        reqContents = '\n'.join(packages)
    elif isinstance(packages, dict):
        # A dictionary of names potentially to versions
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
        # Straight up string
        reqContents = packages

    return reqContents

