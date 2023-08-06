#!/usr/bin/env python3
# -*- coding: utf-8 -*- Time-stamp: <2020-11-27 09:49:10 sander>*-

# - tutorial:
#   https://packaging.python.org/tutorials/packaging-projects
# - full documentation:
#   https://packaging.python.org/guides/distributing-packages-using-setuptools
# - more hints:
#   http://shallowsky.com/blog/programming/developing-pypi-project.html
#   https://realpython.com/pypi-publish-python-package

# ----------------------------------------------------------------------------

import setuptools
import re
import sys

# ----------------------------------------------------------------------------

# - write README.md in GitHub Flavored Markdown language:
#   https://gist.github.com/stevenyap/7038119
#   https://jbt.github.io/markdown-editor
#   https://github.github.com/gfm
with open('README.md', 'r') as f:
    long_description = f.read()

# ----------------------------------------------------------------------------

# get version number from asyroro.py:
# https://packaging.python.org/guides/single-sourcing-package-version
def get_version():
    with open('asyroro/asyroro.py', 'r') as f:
        for line in f:
            result = re.search('^\s*__version__\s*=\s*[\'"]([0-9.]+)[\'"]', line)
            if (result):
                return result.group(1)
    sys.exit('ERROR: No version number found.')

# ----------------------------------------------------------------------------

setuptools.setup(
    name                          = 'asyroro',
    version                       = get_version(),
    author                        = 'Rolf Sander',
    author_email                  = 'mail@rolf-sander.net',
    description                   = 'ASYnchronous ROund-RObin tournaments',
    long_description              = long_description,
    long_description_content_type = 'text/markdown',
    url                           = 'http://www.rolf-sander.net/software/asyroro',
    packages                      = setuptools.find_packages(),
    install_requires              = ['numpy'],
    scripts                       = ['asyroro/asyroro.py'],
    classifiers                   = [ # https://pypi.org/classifiers
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Mathematics',
        ],
    python_requires               = '>=3.6',
)

# ----------------------------------------------------------------------------
