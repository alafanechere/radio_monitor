# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='Radio Monitor',
    version='0.0.1',
    description='French radio tracklisting monitoring',
    long_description=readme,
    author='Augustin Lafanechere',
    packages=find_packages(exclude=('tests', 'docs'))
)