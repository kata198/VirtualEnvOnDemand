#!/usr/bin/env python

import sys

from VirtualEnvOnDemand import enableOnDemandImporter, ensureImportGlobal

# Activate the hook
enableOnDemandImporter()

# The following imports are not available without external installation
import IndexedRedis
from AdvancedHTMLParser.exceptions import *

# The following import will go into the global venv where the module and package have different names

Bio = ensureImportGlobal('Bio', 'biopython')

try:
    import mODULEdoesNotExist
except ImportError: 
    sys.stdout.write('Got import error on really non-existant module, as expected.\n')

if __name__ == '__main__':
    sys.stdout.write('IndexedRedis version: ' + IndexedRedis.__version__ + '\n')
    import AdvancedHTMLParser
    sys.stdout.write('AdvancedHTMLParser version: ' + AdvancedHTMLParser.__version__ + '\n')

