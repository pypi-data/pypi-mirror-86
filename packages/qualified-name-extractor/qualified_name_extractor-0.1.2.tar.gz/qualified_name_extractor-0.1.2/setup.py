#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lv Gang
@Email: 1547554745@qq.com
@Created: 2020/11/19
------------------------------------------
@Modify: 2020/11/19
------------------------------------------
@Description:
"""
from setuptools import setup, find_packages

packages = find_packages(exclude=("script", "test*", "test"))

setup(
    name="qualified_name_extractor",
    version="0.1.2",
    keywords=["extract", "qualified name", "extractor"],
    description="extract qualified name",
    long_description="extract qualified name",
    license="Apache License, Version 2.0",

    url="https://github.com/FudanSELab/ExtractQualifiedName",
    author="FDSEKG",
    author_email="1547554745@qq.com",

    packages=packages,
    package_data={
        # If any package contains *.json files, include them:
        '': ['*.json', ".zip"],
    },
    platforms="any",
    install_requires=[
        "sekg",
        "javalang",
        "nltk"
    ]
)
