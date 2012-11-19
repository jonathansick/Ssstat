#!/usr/bin/env python

PROJECT = 'Ssstat'

# Change docs/sphinx/conf.py too!
VERSION = '0.0.2'

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

from distutils.util import convert_path
from fnmatch import fnmatchcase
import os
import sys

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='S3 Analytics in MongoDB',
    long_description=long_description,

    author='Jonathan Sick',
    author_email='jonathansick@mac.com',

    url='https://github.com/jonathansick/Ssstat',
    download_url='https://github.com/jonathansick/Ssstat/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['distribute', 'cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'ssstat = ssstat.main:main'
        ],
        'ssstat.app': [
            'ingest = ssstat.ingest:IngestCommand',
            # 'recover = ssstat.recover:RecoverCommand',
        ],
    },

    zip_safe=False,
)
