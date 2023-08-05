#!/usr/bin/env python3

# Note!
# ' are required, do not use any ".

# setup.
from setuptools import setup, find_packages
setup(
	name='h3roku',
	version='0.1.1',
	description='Some description.',
	url="http://github.com/vandenberghinc/h3roku",
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
		"cl1",
		"fil3s",
		"r3sponse",
	])