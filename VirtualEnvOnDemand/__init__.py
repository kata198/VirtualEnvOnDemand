# Copyright (c) 2015 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
#
#  VirtualEnvOnDemand provides a simple means for an application, without restarting, to temporarily install and use its runtime requirements  

# vim: ts=4 sw=4 expandtab


from .exceptions import PipInstallFailed

__all__ = ('createEnv', 'createEnvIfCannotImport', 'enableOnDemandImporter', 'installPackages', 'PipInstallFailed', '__version__', '__version_tuple__')

__version__ = '2.0.1'
__version_tuple__ = (2, 0, 1)

from .CreateEnv import createEnv, createEnvIfCannotImport

from VirtualEnvOnDemand.GlobalEnv import enableOnDemandImporter
from VirtualEnvOnDemand.InstallPackages import installPackages
