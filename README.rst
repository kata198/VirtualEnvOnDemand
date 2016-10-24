VirtualEnvOnDemand
==================

VirtualEnvOnDemand contains two primary parts:

**Managing Environments**

  VirtualEnvOnDemand provides a simple means for an application or series of applications to create a persistent OR temporary
    virtual environment (virtualenv), install packages within that environment, activate it, etc.

**On-Demand importing**

  VirtualEnvOnDemand also provides an "on demand" importer, which allows you to automatically install providing packages
   when imports fail

Using VirtualEnvOnDemand allows you to be explicit and pythonify your virtualenv deployment and required packages,
and not rely on a "black box" of the target system to provide your deps, nor are you forced to couple creating/transferring 
a virtualenv with your program.

It also allows you to easily share scripts/applications with others, without requiring them to have any dependencies (other than virtualenv)
installed on their system. They also do not need to know how to create virtualenvs, rely on them being active, etc.

Managing Virtualenvs / Persistent Virtualenvs
---------------------------------------------

You can use VirtualEnvOnDemand to create a virtualenv post-deployment, to both make explicit your dependencies/virtualenv setup,

and to ensure that on any target system your project can run, so long as virtualenv is installed.

The general idea is that your project contains a file, like "venv.py", which your application will import.

Upon import, this file will create the env if it does not exist, install/update new packages if you so desire, 
and activate the virtualenv, ensuring any and all required dependencies are available to your project.


Example:

	if os.path.isdir('/tmp/MyEnv'):
		myEnvInfo = VirtualEnvOnDemand.getInfoFromVirtualEnv('/tmp/MyEnv')
	else:
		myEnv = VirtualEnvOnDemand.createEnv(packages=['ExamplePackage'], parentDirectory='/tmp', name='MyEnv', deleteOnClose=False)

to create an env in "/tmp" named "MyEnv", with "ExamplePackage" installed by default.

Then, you can use:

	VirtualEnvOnDemand.activateEnv(myEnv)

to activate it (allow imports from this virtualenv).

You can also use the on-demand functionality by calling:

	VirtualEnvOnDemand.setGlobalVirtualEnv(myEnv, enableOnDemandImporter=True)

which will exapand the env you created as-needed, when imports fail.


Full example, with comments: https://github.com/kata198/VirtualEnvOnDemand/blob/master/examples/persistent_venv.py

On-Demand Importing
-------------------

VirtualEnvOnDemand has the ability to automatically attempt to install packages at import-time, when an import fails.

This is recommended for developemnt and quick-and-dirty scripts. For production projects, you should use a persistent environment (see "Persistent Virtualenvs" section above).

You may call *VirtualEnvOnDemand.enableOnDemandImporter()* to add a hook to python imports, and if an import fails, it will try to install the providing package using pip.

The default (controlled by deferSetup flag to *enableOnDemandImporter*) is to not setup the global virtualenv until needed (like when an import fails local). This allows the on demand importer to be used without penality if all requires modules are present, but still gives the robustness to install those that aren't.

Your existing pip.conf provides the options and index url that will be searched.

This works fine and well, so long as modules have the same name as their package. When this is not the case, there are alternative functions.

To handle these using the global env created by *enableOnDemandImporter*, use:

	MyModule = VirtualEnvOnDemand.ensureImportGlobal('MyModule', 'MyPackage')

This will raise "ImportError" if MyModule cannot be imported and MyPackage cannot be installed, or if MyPackage does not provide MyMdoule.

There is more advanced usage, wherein you can create and stack multiple virtualenvs and handle them directory or for certain imports instead of using the global hook. See the documentation link below, and "example\_explicit.py" in the source distribution for more information on that.

**On-Demand Example**

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


**Documentation**

Can be found at:

https://htmlpreview.github.io/?https://raw.githubusercontent.com/kata198/VirtualEnvOnDemand/master/doc/VirtualEnvOnDemand.html




Additional examples can be found in the "examples" directory, https://github.com/kata198/VirtualEnvOnDemand/tree/master/examples
