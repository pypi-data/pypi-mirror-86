# -*- coding: utf-8 -*-
"""credits
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="credits", # Replace with your own username
    version="0.0.1",
    author="Alex Fedotov",
    author_email="alex.fedotov@aol.com",
    description="Verification of data together with meticulous tracing of its' sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alxfed/credits",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)