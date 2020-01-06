# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in somefunctions/__init__.py
from somefunctions import __version__ as version

setup(
	name='somefunctions',
	version=version,
	description='dirty App for some internal testing and correction functions',
	author='itsdave GmbH',
	author_email='dev@itsdave.de',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
