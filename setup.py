#!/usr/bin/env python3
#
# pack setup
#
# date: Mar 1 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


from setuptools import setup, find_packages
#from ama.core.version import get_version

VERSION = "v0.0.1" 

f = open('README', 'r')
LONG_DESCRIPTION = f.read()
f.close()


setup(
    name='pack_ama',
    version=VERSION,
    description='Password Analysis and Cracking Kit',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    maintainer='glozanoa',
    maintainer_email='glozanoa@uni.pe',
    url='https://github.com/fpolit/pack',
    license='GPL3',
    packages=find_packages(),
    include_package_data=True,
)