import os
import io
from setuptools import find_packages, setup

CURDIR= os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name="enumpaths",
    author="0xBruno",
    author_email="0xbruno90@gmail.com",
    url="https://github.com/0xBruno/enumpaths",
    version="1.0",
    description="simple Python tool iterates through URLs sending a proxied GET request (for Burp).",
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    python_requires='>=3.6',
    keywords=[],
    scripts=[],
    install_requires=["click==7.1.2", "requests==2.25.0"],
    entry_points={ "console_scripts": ["enumpaths=enumpaths.main:cli"]},
)
