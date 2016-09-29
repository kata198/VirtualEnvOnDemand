# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
# 
#  This file contains things related to the "global" env, used for auto-importing.

# vim: ts=4 sw=4 expandtab
import imp
import sys
import tempfile

from .CreateEnv import createEnv, activateEnv
from .InstallPackages import installPackages, ensureImport
from .VirtualEnvInfo import VirtualEnvInfo, VirtualEnvDeferredBuild, getInfoFromVirtualEnv
from .exceptions import VirtualEnvDoesNotExist

__all__ = ('globalOnDemandVirtualEnv', 'isOnDemandImporterEnabled', 'getGlobalVirtualEnvInfo', 'enableOnDemandImporter', 'ensureImportGlobal', 'VirtualEnvOnDemandImporter', 'toggleOnDemandImporter', 'toggleDebug')

global globalOnDemandVirtualEnv
globalOnDemandVirtualEnv = None
global isOnDemandImporterEnabled
isOnDemandImporterEnabled = False
global knownFailures
knownFailures = set()

global debug
debug = False

def toggleDebug(isDebug):
    '''
        toggleDebug - Toggle debug messages. Default disabled.

        @param isDebug <bool> - Whether to enable debug messages or disable them.

        @return <bool> - The old state of debug
    '''
    global debug

    oldValue = debug

    debug = isDebug
    return oldValue

def getGlobalVirtualEnvInfo():
    '''
        getGlobalVirtualEnvInfo - Returns the VirtualEnvInfo object representing the global environment, or None if not setup.

        If not setup, call enableOnDemandImporter() to add the hook and create the "global" env.

        @return VirtualEnvInfo representing global env, or None if enableOnDemandImporter has not been called.
    '''
    return globalOnDemandVirtualEnv

def setGlobalVirtualEnv(venv, enableOnDemandImporter=True):
    '''
        setGlobalVirtualEnv - Sets the global virtualenv to be used by the on demand importer.

        @param venv <str/VirtualEnvInfo> - Either the path to the root of the virtualenv, or a VirtualEnvInfo (like from getInfoFromVirtualEnv)
        @param enableOnDemandImporter <bool> Default True - If True, will enable the on demand importer right away.

        @return <VirtualEnvInfo> - The global env
    '''
    global globalOnDemandVirtualEnv
    if not isinstance(venv, VirtualEnvInfo):
        venv = getInfoFromVirtualEnv(venv)

    globalOnDemandVirtualEnv = venv

    activateEnv(venv)
    if enableOnDemandImporter:
        toggleOnDemandImporter(True)

    return globalOnDemandVirtualEnv


def enableOnDemandImporter(tmpDir=None, deferSetup=True, noRetryFailedPackages=True):
    '''
        enableOnDemandImporter - Calling this method turns on the "on demand" importer. A temporary global env is created, and all failed imports will attempt an installation.

           @param tmpDir <str/None> - Temporary directory to use. A subdirectory will be created within this. Defaults to tempfile.gettempdir()
           @param deferSetup <bool> - If True (default), defers setup (which can take a couple seconds) until the first failed import or attempted install.
                                        Setup takes a couple seconds. Use this to always enable on-demand importer, but give advantage if all modules are present.
                                        If False, the ondemand virtualenv will be setup right-away. If you are using this in a multi-threaded environment, this should be set to False.
           @param noRetryFailedPackages <bool> - If True (default), a package which fails to download will not be retried. This is a performance savings. This should generally always be True,
                                                   unless you are using VirtualEnvOnDemand to have a running process written to work with an unreleased module to prevent a restart or something similar.
    '''
    global isOnDemandImporterEnabled, globalOnDemandVirtualEnv, knownFailures
    if isOnDemandImporterEnabled is True:
        return
    if deferSetup is False:
        globalOnDemandVirtualEnv = createEnv(packages=None, parentDirectory=tmpDir, stdout=None, stderr=None)
    else:
        globalOnDemandVirtualEnv = VirtualEnvDeferredBuild(parentDirectory=tmpDir or tempfile.gettempdir())

    if noRetryFailedPackages is False:
        knownFailures = None

    sys.meta_path = [VirtualEnvOnDemandImporter()] + sys.meta_path
    isOnDemandImporterEnabled = True


def toggleOnDemandImporter(isActive):
    '''
        toggleOnDemandImporter - Toggle whether the on demand importer (import hook) is active.

            If enableOnDemandImporter was not ever called, this has no effect. Otherwise, calling toggleOnDemandImporter(False) will temporarily disable the import hook, until toggleOnDemandImporter(True) is called.

            @param isActive <bool> - To temporarily enable/disable the on-demand importer.

            @return <bool> - True if a toggle occured, False if no state has changed.

            @raises ValueError - If no global virtualenv has been set, either by enableOnDemandImporter or setGlobalVirtualEnv
    '''
    global isOnDemandImporterEnabled

    # Make sure we are setup
    if not globalOnDemandVirtualEnv and isActive:
        raise ValueError('toggleOnDemandImporter(True) called, but no globalOnDemandVirtualEnv was set! Call enableOnDemandImporter or setGlobalVirtualEnv first!')

    # Check if we already have the desired state
    if not isOnDemandImporterEnabled and not isActive:
        return False

    if isActive is True:
        # We are toggling ON, check if we are already in sys.meta_path so we don't add twice.
        foundIt = False
        for mp in sys.meta_path:
            if issubclass(mp.__class__, VirtualEnvOnDemandImporter):
                foundIt = True
                break
        if not foundIt:
            sys.meta_path = [VirtualEnvOnDemandImporter()] + sys.meta_path
        else:
            return False
    else:
        newMetaPath = []
        for mp in sys.meta_path:
            if issubclass(mp.__class__, VirtualEnvOnDemandImporter):
                continue
            newMetaPath.append(mp)
        sys.meta_path = newMetaPath

    return True
        
    
        


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
        if isinstance(globalOnDemandVirtualEnv, VirtualEnvDeferredBuild):
            toggleOnDemandImporter(False)
            globalOnDemandVirtualEnv = createEnv(packages=None, parentDirectory=globalOnDemandVirtualEnv.virtualenvDirectory, stdout=None, stderr=None)
            toggleOnDemandImporter(True)
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
            if debug is True:
                sys.stderr.write('Skipping %s because in known-failure list\n' %(moduleName,))
            return None

        global globalOnDemandVirtualEnv
        if isinstance(globalOnDemandVirtualEnv, VirtualEnvDeferredBuild):
            # Virtualenv build was deferred, so go ahead and do it.

            # We need to disable our custom importer while building the virtualenv
            toggleOnDemandImporter(False)
            globalOnDemandVirtualEnv = createEnv(packages=None, parentDirectory=globalOnDemandVirtualEnv.virtualenvDirectory, stdout=None, stderr=None)
            toggleOnDemandImporter(True)
            
            
        try:
            installPackages(moduleName, globalOnDemandVirtualEnv['virtualenvDirectory'], None, None)
        except:
#            msg = 'VirtualEnvOnDemand: Unable to resolve and install package to satisfy %s.' %(moduleName,)
#            sys.stderr.write(msg + '\n')
            pass
        if knownFailures is not None:
            knownFailures.add(moduleName)

        return None
