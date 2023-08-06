#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import Command, setup, find_packages

# Package meta information
NAME = "embox"
DESCRIPTION = "Fundamentals of Electromagnetic with Python"
EMAIL = "codequote@163.com"
URL = "https://github.com/WilliamCodeBox/embox"
AUTHOR = "WilliamCodeBox"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.11"
LICENSE = "GNU General Public License v3 (GPLv3)"

# Required packages for this module to be executed
REQUIRED = [
    "numpy>=1.19.2",
    "scipy>=1.5.2",
    "mpi4py>=3.0.3"
]

# Optional packages
EXTRAS = {
    "postprocessor": ["matplotlib>=3.3.2"],
    "test": ["coverage>=5.3.0"]
}

# ######################## Functionalities ########################
here = os.path.abspath(os.path.dirname(__file__))

# Import README and use it as the long-description
# NOTE: this will only work if 'README.md' is present in MANIFEST.in file
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload"""
    description = "Build and publish the package"
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold"""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system(
            "{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine")
        os.system("twine upload dist/*")

        self.status("Pushing git tag...")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.test.*", "tests.*", "notes"]),
    # if only single module exists, use `py_modules` instead of `packages`
    # py_modules = ["embox"]

    # entry_point={
    #     "console_scripts": ["mycli=mymodule:cli"],
    # }

    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: MacOS",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    # setup.py publish support
    cmdclass={
        "upload": UploadCommand,
    }
)
