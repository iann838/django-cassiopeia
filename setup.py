#!/usr/bin/env python

import sys

from setuptools import setup, find_packages


install_requires = [
    "datapipelines>=1.0.7",
    "merakicommons>=1.0.7",
    "Pillow",
    "arrow",
    "requests",
    "Django>=2.2.0",
]

# Require python 3.6
if sys.version_info.major != 3 and sys.version_info.minor != 6:
    sys.exit("'django-cassiopeia' requires Python >= 3.6!")

setup(
    name="django-cassiopeia",
    version="1.0.0", 
    author="Paaksing",
    author_email="paaksingtech@gmail.com",
    url="https://github.com/paaksing/django-cassiopeia",
    description="Django Integration of the Riot Games Developer API Wrapper 'cassiopeia'",
    keywords=["Django", "LoL", "League of Legends", "Riot Games", "API", "REST"],
    classifiers=[
        "Development Status :: 1 - Beta",
        "Programming Language :: Python :: 3",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    packages=find_packages(),
    zip_safe=True,
    install_requires=install_requires,
    include_package_data=True
)
