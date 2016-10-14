# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
#
#  VirtualEnvOnDemand provides a simple means for an application, without restarting, to temporarily install and use its runtime requirements  

# vim: ts=4 sw=4 expandtab



__all__ = ('createEnv', 'createEnvIfCannotImport', 'enableOnDemandImporter', 'getGlobalVirtualEnvInfo', 'installPackages', 'ensureImport', 'ensureImportGlobal', 'PipInstallFailed', 'VirtualEnvInfo', 'toggleOnDemandImporter', 'getInfoFromVirtualEnv', 'activateEnv', 'setGlobalVirtualEnv', 'toggleDebug', )

__version__ = '5.0.4'
__version_tuple__ = (5, 0, 4)

from .exceptions import PipInstallFailed
from .VirtualEnvInfo import VirtualEnvInfo, getInfoFromVirtualEnv

from .CreateEnv import createEnv, createEnvIfCannotImport, activateEnv

from VirtualEnvOnDemand.InstallPackages import installPackages, ensureImport
from VirtualEnvOnDemand.GlobalEnv import enableOnDemandImporter, getGlobalVirtualEnvInfo, ensureImportGlobal, toggleOnDemandImporter, setGlobalVirtualEnv, toggleDebug
