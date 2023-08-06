#!/usr/bin/env python3

from setuptools import Command
from setuptools import setup
import os
import re
import subprocess
import sys


class VersionCheckCommand(Command):
    """Make sure git tag and version match before uploading"""
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        version = self.distribution.get_version()
        version_git = subprocess.check_output(['git', 'describe', '--tags', '--always']).rstrip().decode('utf-8')
        if version != version_git:
            print('ERROR: Release version mismatch! setup.py (%s) does not match git (%s)'
                  % (version, version_git))
            sys.exit(1)
        print('Upload using: twine upload --sign dist/fdroidserver-%s.tar.gz' % version)


with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='drcontrol',
      version='0.14',
      description='Control Denkovi USB Relay Boards',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Sebastian Sjoholm',
      author_email='sebastian.sjoholm@gmail.com',
      license='GPL-3.0',
      scripts=['drcontrol.py'],
      python_requires='>=3.4',
      cmdclass={'versioncheck': VersionCheckCommand},
      install_requires=[
          'pylibftdi',
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Telecommunications Industry',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Topic :: Utilities',
      ],
)
