# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"


# vim: ts=4 sw=4 expandtab

import os
import sys

__all__ = ('VirtualEnvInfo', 'getInfoFromVirtualEnv')


class VirtualEnvInfo(object):

    __slots__ = ('virtualenvDirectory', 'sitePackagesDirectory')


    def __init__(self, virtualenvDirectory, sitePackagesDirectory=''):
        '''
            @param virtualenvDirectory <str> - Path to the root of the virtualenv
            @param sitePackagesDirectory <str> - Path to the site packages directory (goes into PYTHONPATH)

            If virtualenvDirectory is provided, sitePackagesDirectory will be calculated with default expected values.

            This object should be considered read-only. If you need to modify values, you must create a new object.


        '''
        if not virtualenvDirectory:
            raise ValueError('virtualenvDirectory is required and must be specified.')

        virtualenvDirectory = os.path.realpath(virtualenvDirectory)

        self.virtualenvDirectory = virtualenvDirectory

        if not sitePackagesDirectory:
            sitePackagesDirectory = VirtualEnvInfo._getSitePackagesDirectory(virtualenvDirectory)

        self.sitePackagesDirectory = sitePackagesDirectory


    @staticmethod
    def _getSitePackagesDirectory(virtualenvDirectory):
        versionInfo = sys.version_info
        return os.sep.join([virtualenvDirectory, 'lib', 'python%d.%d' %(versionInfo.major, versionInfo.minor), 'site-packages'])

    @staticmethod
    def _getPythonBin(virtualenvDirectory):
        return os.sep.join([virtualenvDirectory, 'bin', 'python'])


    def __getitem__(self, name):
        if name == 'virtualenvDirectory':
            return self.virtualenvDirectory
        elif name == 'sitePackagesDirectory':
            return self.sitePackagesDirectory

        raise KeyError('Unknown field: %s. Choices are: %s\n' %(str(name), str(VirtualEnvInfo.__slots__)))


    def validate(self):
        '''
            validate - Validate that the virtualenv exists in the expected way.

            @raises ValueError - With message indicating the reason for failure

            @return <bool> - True
        '''
        if not os.path.isdir(self.virtualenvDirectory):
            raise ValueError('virtualenvDirectory "%s" does not seem to be a directory.' %(self.virtualenvDirectory,))

        pipPath = os.sep.join([self.virtualenvDirectory, 'bin', 'pip'])
        if not os.path.exists(pipPath):
            raise ValueError('Cannot find pip executable at "%s"' %(pipPath,))

        if not os.path.isdir(self.sitePackagesDirectory):
            raise ValueError('Cannot find site packages directory at "%s"' %(self.sitePackagesDirectory,))

        # Validate pip?
        return True

class VirtualEnvDeferredBuild(VirtualEnvInfo):
    '''
        VirtualEnvDeferredBuild - Used by GlobalEnv to defer a build.
    '''

    def __init__(self, parentDirectory):
        self.virtualenvDirectory = parentDirectory
        self.sitePackagesDirectory = None


#   5.0 - Now read only.
#    def __setitem__(self, name, value):
#        if name == 'virtualenvDirectory':
#            self.virtualenvDirectory = value
#        elif name == 'sitePackagesDirectory':
#            self.sitePackagesDirectory = value
#        else:
#            raise KeyError('Unknown field: %s. Choices are: %s\n' %(str(name), str(VirtualEnvInfo.__slots__)))


def getInfoFromVirtualEnv(venvPath, validate=True):
    '''
        getInfoFromVirtualEnv - Gets a VirtualEnvInfo object from a given path.

        @param venvPath <str> - The root of a virtualenv
        @param validate <bool> Default True - If True, will validate that the virtualenv is usable.

        @raises - if validate is True, @see VirtualEnvInfo.validate
    '''
    # sitePackagesDirectory will auto-calculate in VirtualEnvInfo.__init__
    ret = VirtualEnvInfo(venvPath)
    if validate:
        ret.validate()

    return ret

    
