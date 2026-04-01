from setuptools import setup, find_packages
import os

long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="dashcode",
    version="1.2.5",
    packages=find_packages(),
    author="IWiterI",
    description="A library for Geometry Dash level generation using .gmd files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    project_urls={
        "Homepage": "https://github.com/ISviterI/dashcode",
        "Discord": "https://discord.gg/MXv3KTFmPE",
        "Wiki": "https://github.com/ISviterI/dashcode/wiki",
        "Documentation": "https://github.com/ISviterI/dashcode/wiki/Documentation",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='geometry dash, gd, level-generator, automation, 2.2, python, dash, dashcode, code',
)