#!/usr/bin/env python

import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="ud3tn-tools",
    version="0.0.0",
    install_requires=["ud3tn-utils"],
    author="D3TN GmbH",
    author_email="contact@d3tn.com",
    description="Empty package to indicate the preferred use of ud3tn-utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
