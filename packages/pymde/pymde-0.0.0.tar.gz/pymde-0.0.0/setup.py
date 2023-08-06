from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pymde",
    version="0.0.0",
    description="Minimum Distortion Embedding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="Apache License, Version 2.0",
    url="https://github.com/cvxgrp/pymde",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
