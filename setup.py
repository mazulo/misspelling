#!/usr/bin/env python

"""Installer for misspelling-check.

This installs the misspelling command and the misspellings.check module.

"""

import ast
import sys
from distutils.core import Command
from distutils.core import setup
import unittest


def version():
    """Return version string."""
    with open('misspellings_lib_hurkman/__init__.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


class TestCommand(Command):
    description = 'Runs all available tests.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tests = unittest.TestLoader().discover('tests')
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(tests)
        if not result.wasSuccessful():
            sys.exit(1)


with open('README.rst') as readme:
    setup(
        cmdclass={'test': TestCommand},
        name='misspellings_hurkman',
        version=version(),
        url='https://github.com/erichurkman/misspellings',
        download_url='https://github.com/erichurkman/misspellings/tarball/10.2',
        author='Eric Hurkman',
        author_email='erichurkman@gmail.com',
        description='A tool to detect misspellings with opinionated additions',
        long_description=readme.read(),
        packages=['misspellings_lib_hurkman'],
        package_data={'misspellings_lib_hurkman': ['custom.json', 'wikipedia.json']},
        scripts=['misspellings', ],
        keywords='check, code, spelling, spellcheck',
        license='GNU General Public License v3',
        platforms=['POSIX'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Utilities'
        ])
