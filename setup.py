#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from io import open
import re
import sys

from setuptools import find_packages, setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("cli_helpers/__init__.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )


def open_file(filename):
    """Open and read the file *filename*."""
    with open(filename) as f:
        return f.read()


readme = open_file("README.rst")

setup(
    name="cli_helpers",
    author="dbcli",
    author_email="thomas@roten.us",
    version=version,
    url="https://github.com/dbcli/cli_helpers",
    packages=find_packages(exclude=["docs", "tests", "tests.tabular_output"]),
    include_package_data=True,
    description="Helpers for building command-line apps",
    long_description=readme,
    long_description_content_type="text/x-rst",
    install_requires=[
        "configobj >= 5.0.5",
        "tabulate[widechars] >= 0.9.0",
    ],
    extras_require={
        "styles": ["Pygments >= 1.6"],
    },
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals :: Terminal Emulators/X Terminals",
    ],
)
