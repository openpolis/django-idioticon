#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import idioticon

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = idioticon.__version__
description = idioticon.__doc__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-idioticon',
    version=version,
    description=description,
    long_description=readme + '\n\n' + history,
    author='openpolis',
    author_email='lab@openpolis.it',
    url='https://github.com/openpolis/django-idioticon',
    packages=[
        'idioticon',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="MIT",
    zip_safe=False,
    keywords='idioticon',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)