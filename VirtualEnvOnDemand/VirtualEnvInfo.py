# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"


# vim: ts=4 sw=4 expandtab


class VirtualEnvInfo(object):

    __slots__ = ('virtualenvDirectory', 'sitePackagesDirectory', 'requirementsTxt', 'deferredBuildIn')


    def __init__(self, virtualenvDirectory='', sitePackagesDirectory='', requirementsTxt='', deferredBuildIn=''):
        '''
            virtualenvDirectory <str> - Path to the root of the virtualenv
            sitePackagesDirectory <str> - Path to the site packages directory (goes into PYTHONPATH)
            requirementsTxt <str> - The generated requirements.txt for initial setup. May go away, not very useful.
            deferredBuildIn <str> - If set for the global env, the creation of the virtualenv is deferred until needed. This is then the path of the parent directory wherein the venv will be created.
        '''
        self.virtualenvDirectory = virtualenvDirectory
        self.sitePackagesDirectory = sitePackagesDirectory
        self.requirementsTxt = requirementsTxt
        self.deferredBuildIn = deferredBuildIn

    def __getitem__(self, name):
        if name == 'virtualenvDirectory':
            return self.virtualenvDirectory
        elif name == 'sitePackagesDirectory':
            return self.sitePackagesDirectory
        elif name in ('requirements.txt', 'requirementsTxt'):
            return self.requirementsTxt

        raise KeyError('Unknown field: %s. Choices are: %s\n' %(str(name), str(VirtualEnvInfo.__slots__)))

    def __setitem__(self, name, value):
        if name == 'virtualenvDirectory':
            self.virtualenvDirectory = value
        elif name == 'sitePackagesDirectory':
            self.sitePackagesDirectory = value
        elif name in ('requirements.txt', 'requirementsTxt'):
            self.requirementsTxt = value
        else:
            raise KeyError('Unknown field: %s. Choices are: %s\n' %(str(name), str(VirtualEnvInfo.__slots__)))
