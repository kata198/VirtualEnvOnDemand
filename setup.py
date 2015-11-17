#!/usr/bin/env python
#
# Copyright (c) 2015 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"


#vim: set ts=4 sw=4 expandtab

import os
from setuptools import setup


if __name__ == '__main__':

    dirName = os.path.dirname(__file__)
    if dirName and os.getcwd() != dirName:
        os.chdir(dirName)

    summary = 'Provides a simple means for an application, without restarting, to temporarily install and use its runtime requirements'

    try:
        with open('README.rst', 'r') as f:
            long_description = f.read()
    except Exception as e:
        sys.stderr.write('Exception when reading long description: %s\n' %(str(e),))
        long_description = summary

    setup(name='VirtualEnvOnDemand',
            version='2.0.0',
            packages=['VirtualEnvOnDemand'],
            author='Tim Savannah',
            author_email='kata198@gmail.com',
            maintainer='Tim Savannah',
            url='https://github.com/kata198/VirtualEnvOnDemand',
            maintainer_email='kata198@gmail.com',
            requires=['virtualenv'],
            install_requires=['virtualenv'],
            description=summary,
            long_description=long_description,
            license='LGPLv3',
            keywords=['virtualenv', 'on', 'demand', 'pip', 'install', 'import', 'runtime', 'ImportError', 'reload', 'module'],
            classifiers=['Development Status :: 4 - Beta',
                         'Programming Language :: Python',
                         'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                         'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2.6',
                          'Programming Language :: Python :: 2.7',
                          'Programming Language :: Python :: 3',
                          'Programming Language :: Python :: 3.3',
                          'Programming Language :: Python :: 3.4',
                          'Topic :: System :: Installation/Setup',
                          'Topic :: Software Development :: Libraries :: Python Modules',
            ]
    )

