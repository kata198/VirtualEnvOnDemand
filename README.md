VirtualEnvOnDemand
==================

VirtualEnvOnDemand provides a simple means for an application, without restarting, to temporarily install and use its runtime requirements


**How it works**

When you call createEnv, A virtualenv is created (and by default will be removed upon application termination) in a temporary location, 
the given packages (and optionally specific versions) are installed therein, and that additional site-packages directory is prepended 
to your running python module search-path.



**Documentation**

Can be found at:

https://htmlpreview.github.io/?https://raw.githubusercontent.com/kata198/VirtualEnvOnDemand/master/doc/VirtualEnvOnDemand.html



Example:
--------

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
