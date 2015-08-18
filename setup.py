#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pip

from setuptools import setup, find_packages
from pip.req import parse_requirements
import frojd_fabric_cli


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

package_exclude = ("tests*", "examples*")
packages = find_packages(exclude=package_exclude)

with open("README.md") as f:
    readme = f.read()

requires = parse_requirements("requirements/install.txt",
                              session=pip.download.PipSession())
install_requires = [str(ir.req) for ir in requires]

requires = parse_requirements("requirements/tests.txt",
                              session=pip.download.PipSession())
tests_requires = [str(ir.req) for ir in requires]

setup(
    name="frojd_fabric_cli",
    version=frojd_fabric_cli.__version__,
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_requires,
    license="MIT",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "frojd_fabric = frojd_fabric_cli.scripts.init:main",
            "cleanup = frojd_fabric_cli.scripts.cleanup:main",
        ]
    },
)
