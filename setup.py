##############################################################################
#
# Copyright (c) 2010 Tau Productions Inc.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup

"""
NAME = 'tau.selectorstrings'
VERSION = '0.1dev'

import os.path
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

def read(*rnames):
    return open(os.path.join(HERE, *rnames)).read()

setup(
    # Basic Identification of Distribution
    name=NAME,
    version=VERSION,

    # Descriptions for Potential Users of Distribution
    description='ZCML Directive to Define Configuration Strings for Dropdown Lists',
    long_description=(
        read('README.rst')
        + '\n' + read('CHANGES.txt')
    ),

    # Location of Stuff Within Distribution
    packages=find_packages('src'),
    namespace_packages=['tau'],
    include_package_data=True,
    zip_safe=False,
    package_dir={ '': 'src' },

    # Contact and Ownership Information
    author='Jeff Rush',
    author_email='jeff@taupro.com',
    url='http://www.timecastle.net',
    license="ZPL 2.1",

    # Egg Classification Info (strings from http://www.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Zope2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Topic :: Internet :: WWW/HTTP",
        ],
    keywords='zcml utility zope',

    # Dependencies on Other Eggs
    install_requires=[
        'setuptools',
        'Zope2',
        'z3c.autoinclude',  # for automatic-slugs-generation of my dependencies
        ],
    extras_require = dict(
        test = [ # eggs needed for functional tests only
            'zope.testing',            # non-Zope-specific testrunner with support for layers
            'z3c.coverage',            # produces HTML output of coverage data from testrunner
            ],
        ),
    )
