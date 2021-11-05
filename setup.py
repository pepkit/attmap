#! /usr/bin/env python

import os
import sys

from setuptools import setup

PACKAGE = "attmap"

# Additional keyword arguments for setup().
extra = {}


def read_reqs(reqs_name):
    deps = []
    with open(
        os.path.join("requirements", "requirements-{}.txt".format(reqs_name)), "r"
    ) as f:
        for l in f:
            if not l.strip():
                continue
            deps.append(l)
    return deps


DEPENDENCIES = read_reqs("all")

extra["install_requires"] = DEPENDENCIES

with open("{}/_version.py".format(PACKAGE), "r") as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

with open("README.md") as f:
    long_description = f.read()

setup(
    name=PACKAGE,
    packages=[PACKAGE],
    version=version,
    description="Multiple access patterns for key-value reference",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="dict, map, mapping, dot, item, getitem, attr, getattr, key-value, dynamic, mutable, access",
    url="https://github.com/pepkit/{}/".format(PACKAGE),
    author=u"Nathan Sheffield, Vince Reuter, Michal Stolarczyk",
    license="BSD2",
    include_package_data=True,
    test_suite="tests",
    tests_require=read_reqs("dev"),
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
    **extra
)
