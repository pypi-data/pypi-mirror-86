#!/usr/bin/env python

import setuptools
import sys

with open("README.md", "r") as file:
    long_description = file.read()

if not "sdist" in sys.argv:
    sys.exit("\n*** Please use the `pyd3tn` package instead of `pydtn`. "
             "See the description if you are looking for the PoC implementation "
             "mentioned in the Bundle Protocol specification.\n")

setuptools.setup(
    name="pydtn",
    version="0.0.0",
    # install_requires=["pyd3tn"],
    author="D3TN GmbH",
    author_email="contact@d3tn.com",
    description="Empty package to indicate replacement by pyD3TN",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
