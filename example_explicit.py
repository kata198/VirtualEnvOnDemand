#!/usr/bin/env python

import sys
import VirtualEnvOnDemand

# Install module when import error. Automatically added to path for current runtime.
try:
    import IndexedRedis
except ImportError:
    VirtualEnvOnDemand.createEnv(['IndexedRedis', 'redis'], parentDirectory='/tmp', stdout=None, stderr=None)
    import IndexedRedis


if __name__ == '__main__':
    sys.stdout.write('IndexedRedis version: ' + IndexedRedis.__version__ + '\n')

    # Use convenience function for checking import otherwise installing module
    VirtualEnvOnDemand.createEnvIfCannotImport('AdvancedHTMLParser', ['AdvancedHTMLParser'], parentDirectory='/tmp', stdout=None)
    import AdvancedHTMLParser
    sys.stdout.write('AdvancedHTMLParser version: ' + AdvancedHTMLParser.__version__ + '\n')
