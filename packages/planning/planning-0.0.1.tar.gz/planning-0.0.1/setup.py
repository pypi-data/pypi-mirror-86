#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="planning",
    description="Planning algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brean/python-planning",
    version="0.0.1",
    license="BSD-3",
    author="Andreas Bresser",
    packages=find_packages(),
    tests_require=[],
    include_package_data=True,
    install_requires=[],
)
