#!/usr/bin/python
# -*- coding: utf-8 -*-

from imp import load_source
from setuptools import setup

tessera_version = load_source("version", "tessera/version.py")

setup(
    name="git-tessera",
    version=tessera_version.__version__,
    license="GPL",
    description="git intransic issue tracking",
    author="Timo Furrer",
    author_email="tuxtimo@gmail.com",
    maintainer="Timo Furrer",
    maintainer_email="tuxtimo@gmail.com",
    platforms=["Linux", "Windows", "MAC OS X"],
    url="https://github.com/timofurrer/git-tessera2.git",
    download_url="https://github.com/timofurrer/git-tessera2.git",
    install_requires=["click==3.1", "gittle==0.4.0"],
    packages=["tessera"],
    entry_points={"console_scripts": ["git-tessera = tessera.main:cli"]},
    package_dir={"git-tessera": "tessera"},
    #package_data={"templates": ["*"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: Implementation",
        "Topic :: Software Development",
        "Topic :: Software Development :: Bug Tracking"
    ]
)
