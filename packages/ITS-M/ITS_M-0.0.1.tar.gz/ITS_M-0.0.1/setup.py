import os
from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

short_description = "Open source document management system (DMS)"

'''
setup(
    name='ITS_M',
    version="0.0.1",
    packages=find_packages(include=['ITS_M.*']),
    include_package_data=True,
    description=short_description,
    long_description=README,
    long_description_content_type="text/markdown",
    url='http://www.smartcs.co.kr/',
    author='Smartcs',
    author_email='eugen@papermerge.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6')
    '''

setup(
    name='ITS_M',
    version="0.0.1",
    description = short_description,
    Long_description = "this is a example of ITS_M installation",
    author= "smartcs",
    author_email='botyagp@gmail.com',
    url='http://www.smartcs.co.kr/',
    entry_points={},
    package_dir={'': 'ITS_M'},
    packages = find_packages('ITS_M'),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires = [])