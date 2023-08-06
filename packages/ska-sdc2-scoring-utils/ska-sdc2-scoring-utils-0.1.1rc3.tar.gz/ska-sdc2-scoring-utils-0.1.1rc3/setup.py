"""Packaging script for sdc2 scoring utilities.

https://packaging.python.org/tutorials/packaging-projects/
"""
from setuptools import setup, find_packages

with open("README.md", "r") as file:
    README = file.read()

setup(
    author="SKA Organisation",
    name="ska-sdc2-scoring-utils",
    version="0.1.1rc3",
    description="Utility scripts for interacting with SKA SDC2 scoring service.",
    url="https://gitlab.com/ska-telescope/sdc/sdc2-scoring-utils",
    license="License :: OSI Approved :: BSD License",
    long_description=README,
    long_description_content_type="text/markdown",
    scripts=["scripts/sdc2-score", "scripts/sdc2-score-admin"],
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=["python-keycloak", "requests"],
    python_rquires=">=3.6",
    clasifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
)
