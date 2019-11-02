import setuptools
from os import sys
import pypandoc

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

long_description = pypandoc.convert_file('README.md', 'rst')
long_description = long_description.replace("\r", "")

setuptools.setup(
    name="Site Mapper",
    version="0.0.1",
    author="Dave O'Connor",
    author_email="github@dead-pixels.org",
    description="Script/API to read and parse sitemap.xml data into objects",
    long_description=long_description,
    url="https://github.com/daveoconnor/sitemapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    tests_require=["pytest"],
    setup_requires=[] + pytest_runner,

)