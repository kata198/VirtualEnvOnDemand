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


**Persistent Environment**

You can use VirtualEnvOnDemand to create a virtualenv post-deployment, to both make explicit your dependencies/virtualenv setup,

and to ensure that on any target system your project can run, so long as virtualenv is installed.

The general idea is that your project contains a file, like "venv.py", which your application will import.

Think of it like a django settings.py, but for virtualenv and package dependencies.

For most cases, your venv.py can consistent of a single call to the following method:

	def setupAndActivateEnv(parentDirectory, name, packages, myVersion=None, forceInstallPackages=False, enableOnDemandImporter=False, printDebug=False):
		'''
			setupAndActivateEnv - 

				@param parentDirectory <str> - This is the directory wherein the virtualenv will be created
				@param name <str> - This is the name of the virtualenv root folder
				@param packages <list/dict/str> - A list of packages to install. You can use pip modifiers, like '==' and '<'. May be any of the following:

					List   - A list/tuple/set of package names (optionally including version requirements, e.x. MyPkg==1.2.3)
					Dict   - A dictionary of package names to versions. If no value is present (i.e. evaluates to False, like '' or None), the latest will be fetched.
					String - Directly becomes contents of requirements.txt file to be ingested by pip

				  Note: if the virtualenv exists already, updates to this field will go unnoticed unless 
					"myVersion" increases, or "forceInstallPackages" is set. @see #myVersion parameter below.

					You can also use  " VirtualEnvOnDemand.installPackages( packages, venvInfo ) "  to force install/update of #packages ,
					 where "venvInfo" is the return of this function.
					@see #VirtualEnvOnDemand.InstallPackages.installPackages

				@param myVersion <str/int> - Any sort of version string. You can use __version__ from your module if you so please. Use None to disable.

					When defined, this represents your virtualenv's "version".

					If you are inheriting an existing virtualenv, and this method is passed a higher #myVersion than is currently marked in the
					  virtualenv directory, this method will attempt to install/update any packages as found in #packages.

				@param forceInstallPackages <bool> Default False - If True, will attempt to install/update any packages found in #packages every time.

					On production and deployed code, you will likely want to leave this as False, as it carries a performence penality with every script invocation
					  to check for updates. Instead, bump the value of "myVersion" e.g. from "1.2.0" to "1.2.0.1" or similar, or 
					  explicitly call #VirtualEnvOnDemand.InstallPackages.installPackages from an admin servlet, for example.

				@param enableOnDemandImporter <bool> Default False - If True, will use this env as the global "on demand" importer. 
					@see #VirtualEnvOnDemand.GlobalEnv.enableOnDemandImporter

				@param printDebug <bool> Default False - If True, will print debug messages about what's going on to stderr.
		'''

For example:

	from VirtualEnvOnDemand import setupAndActivateEnv
	import tempfile

	# Import version from module to use below
	from MyProject import __version__ as myProjectVersion

	MY_PACKAGES = ['AdvancedHTMLParser', 'IndexedRedis']

	setupAndActivateEnv(tempfile.gettempdir(), 'MyProjectEnv', MY_PACKAGES, myVersion=myProjectVersion, forceInstallPackages=False, enableOnDemandImporter=False, printDebug=False)


And that's it! Simply put the above into a "venv.py" or similar, and import it from your module or cgi script or whatever.

If the virtualenv at $tempdir$/MyProjectEnv does not exist, it will be created, and the packages in "MY\_PACKAGES" array will be installed.

When the "myVersion" parameter is changed, (in this example, it is linked to the project's module version), it will check that all packages in "MY\_PACKAGES" are installed
and at the latest version.


**Activate a virtualenv**

You can activate any virtualenv by path, and even activate multiple virtualenvs (unlike from the shell "activate" method.)

Simple call *VirtualEnvOnDemand.activateEnv* with a given path

Example:

	from VirtualEnvOnDemand import activateEnv

	activateEnv('/path/to/env')


**Install Packages into a Virtualenv**

You can explicitly cause packages to be installed/updated by using the "installPackages" method.

	def installPackages(packages, venvDir, stdout=sys.stdout, stderr=sys.stderr):
		'''
			installPackages - Installs packages into a created virtual environment

				@param packages - Describes the required packages. Takes one of the following forms:

					String - Directly becomes contents of requirements.txt file to be ingested by pip
					List   - A list/tuple/set of package names (optionally including version requirements, e.x. MyPkg==1.2.3)
					Dict   - A dictionary of package names to versions. If no value is present, the latest will be fetched.

				@param venvDir <str/VirtualEnvInfo> - Path to a created virtualenv directory. This should be the 'virtualenvDirectory' key from the return of createEnv, or just the VirtualEnvInfo object itself will work.
				@param stdout <iostream/None> - Stream to be used as stdout for installation. Default is sys.stdout. Use "None" to swallow output.
				@param stderr <iostream/None> - Stream to be used as stderr for installation. Default is sys.stderr. Use "None" to swallow output.

				@return - The generated requirements.txt used to install packages.

				@raises - 
					VirtualEnvOnDemand.exceptions.PipInstallFailed -  if cannot install packages
					VirtualEnvOnDemand.exceptions.VirtualEnvDoesNotExist - If given venvDir does not exist
					Others (Exception, etc)                        -  If permissions problem to write to specified directory, etc
		'''


For example:

	from VirtualEnvOnDemand import installPackages

	installPackages(['SimpleHttpFetch', '/path/to/env', stdout=None, stderr=None)


You can also attempt to install/update a package only if an import fails, with the "ensureImport" method instead of the "import" keyword.

	def ensureImport(importName, venvDir, packageName=None, stdout=None, stderr=None):
		'''
			ensureImport - Try to import a module, and upon failure to import try to install package into provided virtualenv

			@param importName <str> - The name of the module to import
			@param venvDir <str/VirtualEnvInfo> - The path to a virtualenv, likely created by createEnv or the global env (fetched via getGlobalVirtualEnvInfo()).
			@param packageName <str/None> - If the package name differs from the import name (like biopython package provides "Bio" module), install this package if import fails. This may contain version info (like AdvancedHTMLParser>6.0)
			@param stdout <stream/None> - Stream to use for stdout as package info, or None to silence. Default None. NOTE: This differs from elsewhere where sys.stdout is default.
			@param stderr <stream/None> - Stream to use for stderr as package info, or None to silence. Default None. NOTE: This differs from elsewhere where sys.stderr is default.

			@return - The imported module

			@raises - ImportError if cannot import.

				NOTE: With this method, PipInstallFailed will be intercepted and ImportError thrown instead, as this is intended to be a drop-in replacement for "import" when the package name differs.
		'''


For example:

	from VirtualEnvOnDemand import ensureImport

	Bio = ensureImport('Bio', '/path/to/myenv', packageName='biopython')


There are many other methods and useful features, please check out the full documentation for further info (link below, in "Full Documentation" section).


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


**Full Documentation / Pydoc**

Additional methods can be found at:

https://pythonhosted.org/VirtualEnvOnDemand/


Additional examples can be found in the "examples" directory, https://github.com/kata198/VirtualEnvOnDemand/tree/master/examples
