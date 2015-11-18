VirtualEnvOnDemand
==================

VirtualEnvOnDemand provides a simple means for an application, without restarting, to temporarily install and use its runtime requirements.

The primary means to accomplish this is to call "VirtualEnvOnDemand.enableOnDemandImporter()" which will load the hook into the importer. If an import fails, it will attempt to fetch the corrosponding module and install into current runtime.

You can also explicitly create environments and install packages into them (adding to current runtime). See documentation for more details.


**Why?**

There are a multitude of uses for this. You may use it for development, share scripts and updates with others without them having to modify their virtualenv or install global packages.
You can use it for "lightweight" distributions, for example you may use third-party libs for testing, but they don't need to be in your global setup.py "requires", you can just import them
on-demand when you run tests. Or make up your own use!



**Documentation**

Can be found at:

https://htmlpreview.github.io/?https://raw.githubusercontent.com/kata198/VirtualEnvOnDemand/master/doc/VirtualEnvOnDemand.html



Example:
--------

The following example shows using "enableOnDemandImporter" to automatically fetch and install to current runtime any unavailable imports.

	import sys
	from VirtualEnvOnDemand import enableOnDemandImporter

    # Activate the hook
	enableOnDemandImporter()

    # The following imports are not available, and will be installed into current runtime
	import IndexedRedis
	from AdvancedHTMLParser.exceptions import *

	if __name__ == '__main__':
		sys.stdout.write('IndexedRedis version: ' + IndexedRedis.__version__ + '\n')
		import AdvancedHTMLParser
		sys.stdout.write('AdvancedHTMLParser version: ' + AdvancedHTMLParser.__version__ + '\n')

