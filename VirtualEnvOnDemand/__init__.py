# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
'''
  VirtualEnvOnDemand contains two primary parts:

   * Managing Environments *

      VirtualEnvOnDemand provides a simple means for an application or series of applications to create a persistent OR temporary
        virtual environment (virtualenv), install packages within that environment, activate it, etc.

   * On-Demand importing *

      VirtualEnvOnDemand also provides an "on demand" importer, which allows you to automatically install providing packages
       when imports fail

  Using VirtualEnvOnDemand allows you to be explicit and pythonify your virtualenv deployment and required packages,
   and not rely on a "black box" of the target system to provide your deps, nor are you forced to couple creating/transferring 
   a virtualenv with your program.

  It also allows you to easily share scripts/applications with others, without requiring them to have any dependencies (other than virtualenv)
   installed on their system. They also do not need to know how to create virtualenvs, rely on them being active, etc.
'''

# vim: ts=4 sw=4 expandtab



__all__ = ('createEnv', 'createEnvIfCannotImport', 'enableOnDemandImporter', 'getGlobalVirtualEnvInfo', 'installPackages', 'ensureImport', 'ensureImportGlobal', 'PipInstallFailed', 'VirtualEnvInfo', 'toggleOnDemandImporter', 'getInfoFromVirtualEnv', 'activateEnv', 'setGlobalVirtualEnv', 'setupAndActivateEnv', 'toggleDebug', )

__version__ = '5.1.0'
__version_tuple__ = (5, 1, 0)

from .exceptions import PipInstallFailed
from .VirtualEnvInfo import VirtualEnvInfo, getInfoFromVirtualEnv

from .CreateEnv import createEnv, createEnvIfCannotImport, activateEnv

from VirtualEnvOnDemand.InstallPackages import installPackages, ensureImport
from VirtualEnvOnDemand.GlobalEnv import enableOnDemandImporter, getGlobalVirtualEnvInfo, ensureImportGlobal, toggleOnDemandImporter, setGlobalVirtualEnv, toggleDebug

from .PersistentEnv import setupAndActivateEnv
