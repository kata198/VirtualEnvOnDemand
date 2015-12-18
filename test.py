#!/usr/bin/env python

import sys

from VirtualEnvOnDemand import enableOnDemandImporter

# Activate the hook
enableOnDemandImporter()

# The following imports are not available without external installation
import SimpleHttpFetch
from AdvancedHTMLParser.exceptions import *




if __name__ == '__main__':
    sys.stdout.write('SimpleHttpFetch version: ' + SimpleHttpFetch.__version__ + '\n')
    import AdvancedHTMLParser
    sys.stdout.write('AdvancedHTMLParser version: ' + AdvancedHTMLParser.__version__ + '\n')

