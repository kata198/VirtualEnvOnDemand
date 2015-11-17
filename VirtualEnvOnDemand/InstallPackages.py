# Copyright (c) 2015 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
#
#  Package installation methods

import os
import tempfile
import subprocess
import sys

from .exceptions import PipInstallFailed

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

def installPackages(packages, venvDir, stdout=sys.stdout, stderr=sys.stderr):
    '''
        installPackages - Installs packages into a created virtual environment

            @param packages - Describes the required packages. Takes one of the following forms:

                String - Directly becomes contents of requirements.txt file to be ingested by pip
                List   - A list/tuple/set of package names (optionally including version requirements, e.x. MyPkg==1.2.3)
                Dict   - A dictionary of package names to versions. If no value is present, the latest will be fetched.

            @param venvDir <str> - Path to a created virtualenv directory. This should be the 'virtualenvDirectory' key from the return of createEnv
            @param stdout <iostream/None> - Stream to be used as stdout for installation. Default is sys.stdout. Use "None" to swallow output.
            @param stderr <iostream/None> - Stream to be used as stderr for installation. Default is sys.stderr. Use "None" to swallow output.

            @return - The generated requirements.txt used to install packages.

            @raises - 
                VirtualEnvOnDemand.exceptions.PipInstallFailed -  if cannot install packages
                Others (Exception, etc)                        -  If permissions problem to write to specified directory, etc
    '''
    # Get packages
    reqContents = generateRequirementsTxt(packages)

    if reqContents:
        # Derive parent temp directory by the virtualenv directory
        parentDirectory = os.path.dirname(venvDir)

        # Generate a temporary named file for the requirements.txt and feed into pip
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

    return reqContents


