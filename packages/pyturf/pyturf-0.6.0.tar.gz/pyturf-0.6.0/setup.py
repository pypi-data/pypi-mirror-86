import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    __version__ = os.environ["GITHUB_REF"].split("/")[-1]
    print(f"Version: {__version__}")
except KeyError:
    from turf.version import __version__

setup(
    name="pyturf",
    version=__version__,
    description="Python geospatial library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyturf/pyturf",
    author="Diogo Matos Chaves, Steffen Häußler",
    author_email="di.matoschaves@gmail.com",
    packages=[*find_packages(), "turf.utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=["numpy"],
    test_requires=["pytest", "pytest-cov"],
)
