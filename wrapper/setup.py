#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
import sys

# Get the directory of this file
here = os.path.abspath(os.path.dirname(__file__))

# Ensure the wrapper script is executable
wrapper_py = os.path.join(here, "c_formatter_42_wrapper.py")
if os.path.exists(wrapper_py):
    os.chmod(wrapper_py, 0o755)
wrapper_sh = os.path.join(here, "c_formatter_42_wrapper.sh")
if os.path.exists(wrapper_sh):
    os.chmod(wrapper_sh, 0o755)

setup(
    name="c_formatter_42_wrapper",
    version="0.1.0",
    description="A wrapper for c_formatter_42 that resolves Python environment compatibility issues",
    author="Marta",
    author_email="mvigara-@student.42madrid.com",
    url="https://github.com/martamakes/c-formatter-42-ext",
    py_modules=["c_formatter_42_wrapper"],
    scripts=["c_formatter_42_wrapper.py", "c_formatter_42_wrapper.sh"],
    entry_points={
        "console_scripts": [
            "c_formatter_42_wrapper=c_formatter_42_wrapper:main",
        ],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Formatters",
    ],
    keywords="c, formatter, 42, norminette",
    project_urls={
        "Bug Tracker": "https://github.com/martamakes/c-formatter-42-ext/issues",
        "Source Code": "https://github.com/martamakes/c-formatter-42-ext",
    },
)
