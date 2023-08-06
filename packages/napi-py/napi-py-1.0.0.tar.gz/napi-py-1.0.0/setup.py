from distutils.core import setup
from setuptools import find_packages

REQUIREMENTS = [
]

REQUIREMENTS_DEV = [
    "tox==3.*",
    "wheel==0.*",
    "twine"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="napi-py",
    version="1.0.0",
    description="CLI tool for downloading subtitles from napiprojekt.pl",
    author="Mateusz Korzeniowski",
    author_email="emkor93@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emkor/napi-py",
    packages=find_packages(exclude=("test", "test.*")),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS_DEV,
    extras_require={
        "dev": REQUIREMENTS_DEV
    },
    entry_points={
        "console_scripts": [
            "napi-py = napi.main:cli_main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities"
    ],
)
