#!/usr/bin/env python

import os.path
from setuptools import setup, find_packages


requirements_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')


setup(
    name='lily-env',
    description=(
        'Lily extension for managing environment variables, '
        'their validity etc.'),
    version='0.0.3',
    author='CoSphere Tech Team',
    url='https://bitbucket.org/goodai/lily-env',
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        lily_env=lily_env.cli:cli
    ''',
    install_requires=open(requirements_path).readlines(),
    package_data={'': ['requirements.txt']},
    include_package_data=True)
