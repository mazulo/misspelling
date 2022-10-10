#!/usr/bin/env python

"""
Installer for misspelling-check.
This installs the misspelling command and the misspellings check module.
"""

import sys
import unittest

from setuptools import Command, setup

from src.utils import get_version


class TestCommand(Command):
    description = "Runs all available tests."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tests = unittest.TestLoader().discover("tests")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(tests)
        if not result.wasSuccessful():
            sys.exit(1)


with open("README.md", encoding="utf-8") as readme:
    setup(
        cmdclass={"test": TestCommand},
        name="src",
        version=get_version(),
        url="https://github.com/mazulo/misspellings",
        download_url=f"https://github.com/mazulo/misspellings/tarball/{get_version()}",
        author="Patrick Mazulo",
        author_email="pmazulo@gmail.com",
        description="A tool to detect misspellings with opinionated additions",
        long_description=readme.read(),
        packages=["src"],
        package_data={"src": ["assets/custom.json", "assets/wikipedia.json"]},
        scripts=[
            "misspellings",
        ],
        keywords="check, code, spelling, spellcheck",
        license="GNU General Public License v3",
        platforms=["POSIX"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Utilities",
        ],
    )
