#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   SimulAI Project (https://github.com/carosaav/SimulAI).
# Copyright (c) 2020,
# Perez Colo Ivo, Pirozzo Bernardo Manuel, Saavedra Sueldo Carolina
# License: MIT
#   Full Text: https://github.com/carosaav


# =============================================================================
# DOCS
# =============================================================================

"""This file is for distribute and install SimulAI
"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib
import sys

from setuptools import setup


# =============================================================================
# CONSTANTS
# =============================================================================

REQUIREMENTS = ["numpy", "attrs"]

# Install pywin32 if OS is Windows.
if sys.platform.startswith("win"):
    REQUIREMENTS.append("pywin32")

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

with open(PATH / "README.md", encoding="utf-8") as fp:
    LONG_DESCRIPTION = fp.read()

with open(PATH / "simulai" / "__init__.py", encoding="utf-8") as fp:
    for line in fp.readlines():
        if line.startswith("__version__ = "):
            VERSION = line.split("=", 1)[-1].replace('"', "").strip()
            break


DESCRIPTION = "SimulAI - Simulation + Artificial Intelligence"


# =============================================================================
# FUNCTIONS
# =============================================================================


def do_setup():
    setup(
        name="simulai",
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author=[
            "Perez Colo Ivo",
            "Pirozzo Manuel Bernardo",
            "Saavedra Sueldo Carolina",
        ],
        author_email="ivoperezcolo@gmail.com",
        url="https://github.com/carosaav/SimulAI",
        license="MIT",
        keywords=[
            "simulai",
            "simulation",
            "artificial intelligence",
            "decision sciences",
            "optimization",
        ],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.8",
            "Topic :: Scientific/Engineering",
        ],
        packages=["simulai"],
        install_requires=REQUIREMENTS,
    )


if __name__ == "__main__":
    do_setup()
