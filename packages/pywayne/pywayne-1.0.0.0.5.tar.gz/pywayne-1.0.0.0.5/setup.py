#!/usr/bin/env python
# encoding: utf-8

"""
@author: Wayne
@contact: wangye.hope@gmail.com
@software: PyCharm
@file: setup
@time: 2020/3/10 14:38
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#") and not line.startswith("~")]


install_reqs = parse_requirements('requirements.txt')

setuptools.setup(
    name="pywayne",
    version="1.0.0.0.5",
    author="Wayne",
    author_email="wang121ye@hotmail.com",
    description="Some useful tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangyendt/wangye_algorithm_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ],
    dependency_links=[
        'https://pypi.tuna.tsinghua.edu.cn/simple/',
        'http://mirrors.aliyun.com/pypi/simple/',
        'http://pypi.douban.com/simple/',
        'https://pypi.python.org/simple',
        'https://pypi.mirrors.ustc.edu.cn/simple/',
    ],
    install_requires=install_reqs,
    packages=setuptools.find_packages(),
    python_requires='>=3',
)
