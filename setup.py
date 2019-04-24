#! /usr/bin/env python

import os
from setuptools import setup
import sys

PACKAGE = "attmap"

# Additional keyword arguments for setup().
extra = {}


def read_reqs(reqs_name):
    deps = []
    with open(os.path.join(
            "requirements", "requirements-{}.txt".format(reqs_name)), 'r') as f:
        for l in f:
            if not l.strip():
                continue
            #deps.append(l.split("=")[0].rstrip("<>"))
            deps.append(l)
    return deps

#DEPENDENCIES = read_reqs("all")
DEPENDENCIES = []

# 2to3
if sys.version_info >= (3, ):
    extra["use_2to3"] = True
extra["install_requires"] = DEPENDENCIES

with open("{}/_version.py".format(PACKAGE), 'r') as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README formatting.
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError, OSError):
    long_description = open('README.md').read()

setup(
    name=PACKAGE,
    packages=[PACKAGE],
    version=version,
    description="Multiple access patterns for key-value reference",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="dict, map, mapping, dot, item, getitem, attr, getattr, key-value, dynamic, mutable, access",
    url="https://github.com/pepkit/{}/".format(PACKAGE),
    author=u"Nathan Sheffield, Vince Reuter",
    license="BSD2",
    include_package_data=True,
    test_suite="tests",
    tests_require=read_reqs("dev"),
    setup_requires=(["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []),
    **extra
)
