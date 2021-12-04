#!/usr/bin/env python

import sys

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    "datapipelines>=1.0.7",
    "merakicommons>=1.0.7",
    "cassiopeia",
    "Pillow",
    "arrow",
    "requests",
    "Django>=3.0.1",
    "wheel",
]

# Require python 3.6
if sys.version_info.major != 3 and sys.version_info.minor != 6:
    sys.exit("'django-cassiopeia' requires Python >= 3.6!")

setup(
    name="django-cassiopeia",
    version="2.1.1", 
    author="Paaksing",
    author_email="paaksingtech@gmail.com",
    url="https://github.com/paaksing/django-cassiopeia",
    description="Django Integration of the Riot Games Developer API Wrapper 'cassiopeia'",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["Django", "LoL", "League of Legends", "Riot Games", "API", "REST"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
        "Framework :: Django :: 3.0",
    ],
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    zip_safe=True,
    install_requires=install_requires,
    include_package_data=True
)
