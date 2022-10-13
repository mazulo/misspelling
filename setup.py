#!/usr/bin/env python

"""
Installer for misspelling-check.
This installs the misspellings command.
"""

import sys
import unittest
from pathlib import Path

from setuptools import Command, find_packages, setup

from src.misspelling_lib.utils import get_version

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


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


setup(
    cmdclass={"test": TestCommand},
    name="misspellings_lib",
    version=get_version(),
    url="https://github.com/mazulo/misspellings",
    download_url=f"https://github.com/mazulo/misspellings/tarball/{get_version()}",
    author="Patrick Mazulo",
    author_email="pmazulo@gmail.com",
    description="A tool to detect misspellings with opinionated additions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    package_data={"misspelling_lib": ["json_sources/wikipedia.json"]},
    entry_points={"console_scripts": ["misspellings = misspelling_lib.misspellings:main"]},
    install_requires=["typed-argument-parser==1.7.2", "rich==12.6.0"],
    keywords="check, code, spelling, spellcheck",
    license="MIT License",
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
