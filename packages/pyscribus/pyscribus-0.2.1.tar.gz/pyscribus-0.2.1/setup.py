#!/usr/bin/python3
# -*- coding:Utf-8 -*-

import setuptools

with open("../README.pypi.rst", "r") as fh:
    long_description = fh.read()

VERSION = "0.2.1"
DESCRIPTION = "Read, create and update Scribus .sla files."

REQUIRED = ['lxml', 'svg.path']

setuptools.setup(
    name="pyscribus",
    version=VERSION,
    author="Étienne Nadji",
    author_email="etnadji@eml.cc",
    description=DESCRIPTION,
    long_description=long_description,
    packages=setuptools.find_packages(),
    platforms='any',
    license="GNU General Public License v3 or later (GPLv3+)",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Text Processing :: Markup :: XML",
        "Intended Audience :: Developers"
    ],
    project_urls={
        "Documentation": "https://etnadji.fr/pyscribus",
        "Source Code": "https://framagit.org/etnadji/pyscribus",
        "Issue tracker": "https://framagit.org/etnadji/pyscribus/-/issues"
    },
    python_requires='>=3.8',
    install_requires=REQUIRED,
    keywords=["scribus", "sla"],
)

# vim:set shiftwidth=4 softtabstop=4 spl=en:
