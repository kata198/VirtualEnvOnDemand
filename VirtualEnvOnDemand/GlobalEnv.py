# Copyright (c) 2015 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
# 
#  This file contains things related to the "global" env, used for auto-importing.

# vim: ts=4 sw=4 expandtab

import imp
import sys

from .CreateEnv import createEnv
from .InstallPackages import installPackages

global globalOnDemandVirtualEnv
globalOnDemandVirtualEnv = None
isOnDemandImporterEnabled = False


def enableOnDemandImporter(tmpDir=None):
    '''
        enableOnDemandImporter - Calling this method turns on the "on demand" importer. A temporary global env is created, and all failed imports will attempt an installation.

           @param tmpDir <str/None> - Temporary directory to use. A subdirectory will be created within this. Defaults to tempdir.gettmpdir()
    '''
    global isOnDemandImporterEnabled, globalOnDemandVirtualEnv
    if isOnDemandImporterEnabled is True:
        return
    globalOnDemandVirtualEnv = createEnv(packages=None, parentDirectory=tmpDir, stdout=None, stderr=None)
    sys.meta_path = [VirtualEnvOnDemandImporter()] + sys.meta_path
    isOnDemandImporterEnabled = True

class VirtualEnvOnDemandImporter(object):
    '''
        VirtualEnvOnDemandImporter - The workhouse of auto-importing. Upon an import that wouldn't resolve, it will try to install the leading package name using pip.
            Failure will still cause a "cannot import" error, but otherwise things will be installed on-demand.
    '''

    def find_module(self, fullname, path=None):
        # Try to see if already installed or loaded, and fall back to default loader
        if path is not None:
            return None

        if fullname in sys.modules or fullname.split('.')[0] in sys.modules:
            return None

        try:
            imp.find_module(fullname, path)
            return None
        except ImportError:
            try:
                imp.find_module(fullname.split('.')[0], path)
                return None
            except ImportError:
                pass

        # Not already installed and could not find, so try our magic.
        moduleName = fullname.split('.')[0]
        try:
            installPackages(moduleName, globalOnDemandVirtualEnv['virtualenvDirectory'], None, None)
        except:
#            msg = 'VirtualEnvOnDemand: Unable to resolve and install package to satisfy %s.' %(moduleName,)
#            sys.stderr.write(msg + '\n')
            pass

        return None
