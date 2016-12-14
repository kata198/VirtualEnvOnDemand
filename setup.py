#!/usr/bin/env python
#
# Copyright (c) 2015, 2016 Timothy Savannah under terms of LGPLv3. You should have received a copy of this with this distribution as "LICENSE"


#vim: set ts=4 sw=4 expandtab

import os
import sys
from setuptools import setup


if __name__ == '__main__':

    dirName = os.path.dirname(__file__)
    if dirName and os.getcwd() != dirName:
        os.chdir(dirName)

    summary = 'Easily create and use virtualenvs and provides the ability for an application to install and use its runtime dependencies at import time'

    try:
        with open('README.rst', 'rt') as f:
            long_description = f.read()
    except Exception as e:
        sys.stderr.write('Exception when reading long description: %s\n' %(str(e),))
        long_description = summary

    setup(name='VirtualEnvOnDemand',
            version='6.0.0',
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
            keywords=['virtualenv', 'on', 'demand', 'pip', 'install', 'import', 'runtime', 'ImportError', 'reload', 'module', 'package'],
            classifiers=['Development Status :: 5 - Production/Stable',
                         'Programming Language :: Python',
                         'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                         'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2.7',
                          'Programming Language :: Python :: 3',
                          'Programming Language :: Python :: 3.3',
                          'Programming Language :: Python :: 3.4',
                          'Programming Language :: Python :: 3.5',
                          'Programming Language :: Python :: 3.6',
                          'Topic :: System :: Installation/Setup',
                          'Topic :: Software Development :: Libraries :: Python Modules',
                          'Operating System :: Microsoft :: Windows',
                          'Operating System :: POSIX',
                          'Operating System :: Unix',
                          'Operating System :: MacOS',
                          'Operating System :: OS Independent',
            ]
    )

