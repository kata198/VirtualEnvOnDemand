VirtualEnvOnDemand
==================

Provides the ability for an application to install and use its runtime dependencies at import time. This allows for you to distribute python scripts and libraries without the overhead of the end-user needing to setup a virtualenv and install dependencies.

VirtualEnvOnDemand provides a simple means for an application, without restarting, to temporarily install and use its runtime requirements.

The primary means to accomplish this is to call "VirtualEnvOnDemand.enableOnDemandImporter()" which will load the hook into the importer. If an import fails, it will attempt to fetch the corrosponding module and install into current runtime.

You can also explicitly create environments and install packages into them (adding to current runtime). See documentation for more details.


**Why?**

There are a multitude of uses for this. You may use it for development, share scripts and updates with others without them having to modify their virtualenv or install global packages.
You can use it for "lightweight" distributions, for example you may use third-party libs for testing, but they don't need to be in your global setup.py "requires", you can just import them
on-demand when you run tests. Or make up your own use!


**Basic Usage**

The simpliest usage is to call *VirtualEnvOnDemand.enableOnDemandImporter()* which will add a hook to the "*import*" keyword, and if an import can't be resolved locally, it will use pip to try to install it.

The default (controlled by deferSetup flag to *enableOnDemandImporter*) is to not setup the global virtualenv until needed (like when an import fails local). This allows the on demand importer to be used without penality if all requires modules are present, but still gives the robustness to install those that aren't.

Your existing pip.conf provides the options and index url that will be searched.

This works fine and well, so long as modules have the same name as their package. When this is not the case, there are alternative functions.

To handle these using the global env created by *enableOnDemandImporter*, use:

	MyModule = VirtualEnvOnDemand.ensureImportGlobal('MyModule', 'MyPackage')

This will raise "ImportError" if MyModule cannot be imported and MyPackage cannot be installed, or if MyPackage does not provide MyMdoule.

There is more advanced usage, wherein you can create and stack multiple virtualenvs and handle them directory or for certain imports instead of using the global hook. See the documentation link below, and "example\_explicit.py" in the source distribution for more information on that.


**Documentation**

Can be found at:

https://htmlpreview.github.io/?https://raw.githubusercontent.com/kata198/VirtualEnvOnDemand/master/doc/VirtualEnvOnDemand.html



Example:
--------

The following example shows using "enableOnDemandImporter" to automatically fetch and install to current runtime any unavailable imports.

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

