#!/usr/bin/env python3
import os

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="squirrel-battle",
    version="3.14",
    author="ynerant",
    author_email="ynerant@crans.org",
    description="Watch out for squirrel's knifes!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.crans.org/ynerant/squirrel-battle",
    packages=find_packages(),
    license='GPLv3',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console :: Curses",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Games/Entertainment",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={"squirrelbattle": ["assets/*"]},
    entry_points={
        "console_scripts": [
            "squirrel-battle = squirrelbattle.bootstrap:Bootstrap.run_game",
        ]
    }
)
