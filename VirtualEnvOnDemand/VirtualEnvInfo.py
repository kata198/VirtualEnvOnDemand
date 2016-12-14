# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"
'''
    VirtualEnvInfo - Classes/methods which describe a virtualenv
'''


# vim: ts=4 sw=4 expandtab

import os
import platform
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
            sitePackagesDirectory = VirtualEnvInfo.getSitePackagesDirectory(virtualenvDirectory)

        self.sitePackagesDirectory = sitePackagesDirectory


    @staticmethod
    def _getSitePackagesDirectoryUnix(virtualenvDirectory):
        '''
            _getSitePackagesDirectoryUnix - Get the site packages directory on a UNIX system (linux, mac, sun, etc)

            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "site-packages" directory of the virtualenv
        '''
        versionInfo = sys.version_info
        return os.sep.join([virtualenvDirectory, 'lib', 'python%d.%d' %(versionInfo.major, versionInfo.minor), 'site-packages'])

    @staticmethod
    def _getSitePackagesDirectoryWindows(virtualenvDirectory):
        '''
            _getSitePackagesDirectoryWindows - Get the site packages directory on a Windows system

            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "site-packages" directory of the virtualenv
        '''
        return os.sep.join([virtualenvDirectory, 'Lib', 'site-packages'])


    @staticmethod
    def getSitePackagesDirectory(virtualenvDirectory):
        '''
            getSitePackagesDirectory - Get the site packages directory associated with a virtualenv.

            NOTE: This is overridden on import with the platform-specific version.

            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "site-packages" directory of the virtualenv
        '''
        raise NotImplementedError('getSitePackagesDirectory should have been overridden by platform-specific version.')


    @staticmethod
    def _getBinDirUnix(virtualenvDirectory):
        '''
            _getBinDirUnix - Gets the "bin" dir of a virtualenv on UNIX systems,
                i.e. the directory that contains executables.

            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "bin" directory of the virtualenv
        '''

        return os.sep.join([virtualenvDirectory, 'bin'])

    @staticmethod
    def _getBinDirWindows(virtualenvDirectory):
        '''
            _getBinDirWindows - Gets the "bin" dir of a virtualenv on Windows systems,
                i.e. the directory that contains executables.
                
                Note this is named "Scripts" on windows, not "bin"

            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "bin" directory of the virtualenv
        '''
        return os.sep.join([virtualenvDirectory, 'Scripts'])

    @staticmethod
    def getBinDir(virtualenvDirectory):
        '''
            getBinDir - Gets the "bin" dir of a virtualenv
                i.e. the directory that contains executables.

            NOTE: This is overridden on import with the platform-specific version.


            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "bin" directory of the virtualenv
        '''
        raise NotImplementedError('getBinDir should have been overridden by platform-specific version.')


    @staticmethod
    def _getPythonBinUnix(virtualenvDirectory):
        '''
            _getPythonBinUnix - Get the path to the virtualenv python executable on a UNIX system

            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "python" executable associated with the virtualenv
        '''
        return os.sep.join([VirtualEnvInfo.getBinDir(virtualenvDirectory), 'python'])

    @staticmethod
    def _getPythonBinWindows(virtualenvDirectory):
        '''
            _getPythonBinWindows - Get the path to the virtualenv python executable on a Windows system

            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "python" executable associated with the virtualenv
        '''
        return os.sep.join([VirtualEnvInfo.getBinDir(virtualenvDirectory), 'python.exe'])

    @staticmethod
    def getPythonBin(virtualenvDirectory):
        '''
            getPythonBin - Get the path to the virtualenv python executable

            NOTE: This is overridden on import with the platform-specific version.


            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "python" executable associated with the virtualenv
        '''
        raise NotImplementedError('getPythonBin should have been overridden by platform-specific version.')

    @staticmethod
    def _getPipBinUnix(virtualenvDirectory):
        '''
            _getPipBinUnix - Get the path to the pip executable within a virtualenv on a UNIX system

            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "pip" executable associated with the virtualenv
        '''
        return os.sep.join([VirtualEnvInfo.getBinDir(virtualenvDirectory), 'pip'])

    @staticmethod
    def _getPipBinWindows(virtualenvDirectory):
        '''
            _getPipBinUnix - Get the path to the pip executable within a virtualenv on a Windows system

            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "pip" executable associated with the virtualenv
        '''
        return os.sep.join([VirtualEnvInfo.getBinDir(virtualenvDirectory), 'pip.exe'])

    @staticmethod
    def getPipBin(virtualenvDirectory):
        '''
            getPipBin - Get the path to the pip executable within a virtualenv

            NOTE: This is overridden on import with the platform-specific version.


            @param virtualenvDirectory <str> - The path to the root directory of the virtualenv

            @return <str> - Path to the "pip" executable associated with the virtualenv
        '''
        raise NotImplementedError('getPipBin should have been overridden by platform-specific version.')


    # WINDOWS VS LINUX/UNIX COMPAT.
    #  Note, we treat cygwin like unix.
    if not sys.argv or not os.path.basename(sys.argv[0]).lower().startswith('pydoc'):
        # Above conditional prevents pydoc from picking up the platform-specific version.
        if platform.system().lower() == 'windows':
            getBinDir = _getBinDirWindows
            getSitePackagesDirectory = _getSitePackagesDirectoryWindows
            getPythonBin = _getPythonBinWindows
            getPipBin = _getPipBinWindows
        else:
            getBinDir = _getBinDirUnix
            getSitePackagesDirectory = _getSitePackagesDirectoryUnix
            getPythonBin = _getPythonBinUnix
            getPipBin = _getPipBinUnix
        

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

        pipPath = VirtualEnvInfo.getPipBin(self.virtualenvDirectory)
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

    
