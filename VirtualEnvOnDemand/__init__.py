# Copyright (c) 2015 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
#
#  VirtualEnvOnDemand provides a simple means for an application, without restarting, to temporarily install and use its runtime requirements  

# vim: ts=4 sw=4 expandtab



__all__ = ('createEnv', 'createEnvIfCannotImport', 'enableOnDemandImporter', 'getGlobalVirtualEnvInfo', 'installPackages', 'ensureImport', 'ensureImportGlobal', 'PipInstallFailed', 'VirtualEnvInfo', '__version__', '__version_tuple__')

__version__ = '3.0.0'
__version_tuple__ = (3, 0, 0)

from .exceptions import PipInstallFailed
from .VirtualEnvInfo import VirtualEnvInfo

from .CreateEnv import createEnv, createEnvIfCannotImport

from VirtualEnvOnDemand.InstallPackages import installPackages, ensureImport
from VirtualEnvOnDemand.GlobalEnv import enableOnDemandImporter, getGlobalVirtualEnvInfo, ensureImportGlobal
