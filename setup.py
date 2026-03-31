from setuptools import setup, find_packages
import os

# Считываем описание из README.md
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="dashcode",
    version="1.0.0",
    packages=find_packages(),
    author="IWiterI",
    description="A library for Geometry Dash level generation using .gmd files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)