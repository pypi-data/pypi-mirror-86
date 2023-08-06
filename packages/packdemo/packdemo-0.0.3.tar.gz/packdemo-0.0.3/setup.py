#!/usr/bin/env python

sdict = {
    'name': 'packdemo',
    'version': "0.0.3",
    'packages': ['packdemo'],
    'zip_safe': False,
    'install_requires': [],
    'author': 'Nolan Zhao',
    'classifiers': [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python'],
    'scripts': ['packdemo/bin/hello']
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(**sdict)