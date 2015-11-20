# Copyright (c) 2015 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
# 
#  This file contains things related to the "global" env, used for auto-importing.

# vim: ts=4 sw=4 expandtab

import imp
import sys

from .CreateEnv import createEnv
from .InstallPackages import installPackages, ensureImport

__all__ = ('globalOnDemandVirtualEnv', 'isOnDemandImporterEnabled', 'getGlobalVirtualEnvInfo', 'enableOnDemandImporter', 'ensureImportGlobal', 'VirtualEnvOnDemandImporter')

global globalOnDemandVirtualEnv
globalOnDemandVirtualEnv = None
global isOnDemandImporterEnabled
isOnDemandImporterEnabled = False


def getGlobalVirtualEnvInfo():
    '''
        getGlobalVirtualEnvInfo - Returns the VirtualEnvInfo object representing the global environment, or None if not setup.

        If not setup, call enableOnDemandImporter() to add the hook and create the "global" env.

        @return VirtualEnvInfo representing global env, or None if enableOnDemandImporter has not been called.
    '''
    return globalOnDemandVirtualEnv

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

def ensureImportGlobal(importName, packageName=None, stdout=None, stderr=None):
    '''
        ensureImportGlobal - Try to import a module, and upon failure to import try to install package into global virtualenv. This assumes that enableOnDemandImporter has already been called.

        @param importName <str> - The name of the module to import
        @param packageName <str/None> - If the package name differs from the import name (like biopython package provides "Bio" module), install this package if import fails. This may contain version info (like AdvancedHTMLParser>6.0)
        @param stdout <stream/None> - Stream to use for stdout as package info, or None to silence. Default None. NOTE: This differs from elsewhere where sys.stdout is default.
        @param stderr <stream/None> - Stream to use for stderr as package info, or None to silence. Default None. NOTE: This differs from elsewhere where sys.stderr is default.

        @return - The imported module

        @raises - ImportError if cannot import.

            NOTE: With this method, PipInstallFailed will be intercepted and ImportError thrown instead, as this is intended to be a drop-in replacement for "import" when the package name differs.
    '''
    global isOnDemandImporterEnabled
    if isOnDemandImporterEnabled is False:
        raise ValueError('Must call enableOnDemandImporter() before using ensureImportGlobal')

    return ensureImport(importName, getGlobalVirtualEnvInfo(), packageName, stdout, stderr)

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
