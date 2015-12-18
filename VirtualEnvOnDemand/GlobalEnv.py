# Copyright (c) 2015 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
# 
#  This file contains things related to the "global" env, used for auto-importing.

# vim: ts=4 sw=4 expandtab

import imp
import sys
import tempfile

from .CreateEnv import createEnv
from .InstallPackages import installPackages, ensureImport
from .VirtualEnvInfo import VirtualEnvInfo
from .exceptions import VirtualEnvDoesNotExist

__all__ = ('globalOnDemandVirtualEnv', 'isOnDemandImporterEnabled', 'getGlobalVirtualEnvInfo', 'enableOnDemandImporter', 'ensureImportGlobal', 'VirtualEnvOnDemandImporter')

global globalOnDemandVirtualEnv
globalOnDemandVirtualEnv = None
global isOnDemandImporterEnabled
isOnDemandImporterEnabled = False
global knownFailures
knownFailures = set()


def getGlobalVirtualEnvInfo():
    '''
        getGlobalVirtualEnvInfo - Returns the VirtualEnvInfo object representing the global environment, or None if not setup.

        If not setup, call enableOnDemandImporter() to add the hook and create the "global" env.

        @return VirtualEnvInfo representing global env, or None if enableOnDemandImporter has not been called.
    '''
    return globalOnDemandVirtualEnv

def enableOnDemandImporter(tmpDir=None, deferSetup=True, noRetryFailedPackages=True):
    '''
        enableOnDemandImporter - Calling this method turns on the "on demand" importer. A temporary global env is created, and all failed imports will attempt an installation.

           @param tmpDir <str/None> - Temporary directory to use. A subdirectory will be created within this. Defaults to tempfile.gettempdir()
           @param deferSetup <bool> - If True (default), defers setup (which can take a couple seconds) until the first failed import or attempted install.
                                        Setup takes a couple seconds. Use this to always enable on-demand importer, but give advantage if all modules are present.
                                        If False, the ondemand virtualenv will be setup right-away.
           @param noRetryFailedPackages <bool> - If True (default), a package which fails to download will not be retried. This is a performance savings. This should generally always be True,
                                                   unless you are using VirtualEnvOnDemand to have a running process written to work with an unreleased module to prevent a restart or something similar.
    '''
    global isOnDemandImporterEnabled, globalOnDemandVirtualEnv, knownFailures
    if isOnDemandImporterEnabled is True:
        return
    if deferSetup is False:
        globalOnDemandVirtualEnv = createEnv(packages=None, parentDirectory=tmpDir, stdout=None, stderr=None)
    else:
        globalOnDemandVirtualEnv = VirtualEnvInfo(deferredBuildIn=tmpDir or tempfile.gettempdir())

    if noRetryFailedPackages is False:
        knownFailures = None

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
    global isOnDemandImporterEnabled, globalOnDemandVirtualEnv
    if isOnDemandImporterEnabled is False:
        raise ValueError('Must call enableOnDemandImporter() before using ensureImportGlobal')

    try:
        return ensureImport(importName, globalOnDemandVirtualEnv, packageName, stdout, stderr)
    except VirtualEnvDoesNotExist as e:
        if globalOnDemandVirtualEnv.deferredBuildIn:
            globalOnDemandVirtualEnv = createEnv(packages=None, parentDirectory=globalOnDemandVirtualEnv.deferredBuildIn, stdout=None, stderr=None)
            return ensureImport(importName, globalOnDemandVirtualEnv, packageName, stdout, stderr)
        else:
            raise
        
        

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
        if knownFailures and moduleName in knownFailures:
            # We are tracking failures and already know this has failed
            sys.stderr.write('Skipping %s because in known-failure list\n' %(moduleName,))
            return None

        global globalOnDemandVirtualEnv
        if globalOnDemandVirtualEnv.deferredBuildIn:
            # Virtualenv build was deferred, so go ahead and do it.
            globalOnDemandVirtualEnv = createEnv(packages=None, parentDirectory=globalOnDemandVirtualEnv.deferredBuildIn, stdout=None, stderr=None)
            
        try:
            installPackages(moduleName, globalOnDemandVirtualEnv['virtualenvDirectory'], None, None)
        except:
#            msg = 'VirtualEnvOnDemand: Unable to resolve and install package to satisfy %s.' %(moduleName,)
#            sys.stderr.write(msg + '\n')
            pass
        if knownFailures is not None:
            knownFailures.add(moduleName)

        return None
