# -*- coding: utf-8 -*-
# @Time : 2020/11/19 下午4:07
# @File : setup.py

from __future__ import print_function

from setuptools import setup

setup(
    name="RyzenUtil",
    version="0.0.2",
    author="张东旭",
    author_email="774270974@qq.com",
    description="common util",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://pypi.org/manage/project/ryzenutil/releases/",
    packages=['code'],
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
)
