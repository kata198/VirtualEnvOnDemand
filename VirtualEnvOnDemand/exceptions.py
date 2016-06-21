# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"

# vim: ts=4 sw=4 expandtab

__all__ = ('PipInstallFailed', 'VirtualEnvDoesNotExist')

class PipInstallFailed(Exception):
    '''
        PipInstallFailed - Exception raised when pip fails to install a list of packages
    '''

    def __init__(self, returnCode=None, reqFileContents=''):
        '''
            Create a PipInstallFailed exception, building a message from some pieces of information

                @param returnCode <int> - Return code of subprocess, or None if undetermined
                @param reqFileContents <str> - String of requirements file to reproduce error
        '''
        self.returnCode = returnCode
        self.reqFileContents = reqFileContents
        Exception.__init__(self, self._genMsg())

    def _genMsg(self):
        return 'Failed to install pip modules (ret=%s) using this requirements file: \n"""\n%s\n"""\n\nCheck stdout/stderr logs.' %(str(self.returnCode), str(self.reqFileContents))


class VirtualEnvDoesNotExist(Exception):
    '''
        VirtualEnvDoesNotExist - Exception raised when an attempt to install into a virtualenv directory that does not exist
    '''
