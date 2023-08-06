#!/usr/bin/env python
"""
Created on 18-12-2012

@author: maciag.artur
@author: jan.danecki
"""
import os.path
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """Command to run unit tests after in-place build."""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '-s', 'tests', '--pep8', '--cov', 'wykop', '--cov-report',
            'term-missing', '--cov-report', 'html',
        ]
        self.test_suite = True

    def run_tests(self):
        # Importing here, `cause outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def read_requirements(filename):
    dirname = os.path.dirname(__file__)
    filename_full = os.path.join(dirname, filename)
    with open(filename_full) as f:
        for line in f:
            if not line or line.startswith('#'):
                continue
            yield line


requires = list(read_requirements('requirements.txt'))
tests_requires = list(read_requirements('requirements_test.txt'))

setup(
    name='wykop-sdk-reborn',
    version='0.1.0',
    packages=find_packages(),
    cmdclass={'test': PyTest},

    # PyPI metadata
    author='Jan Danecki',
    author_email='janek@projmen.pl',
    description='Client library for Wykop API v2',
    long_description=open("README.md").read(),
    url='https://github.com/krasnoludkolo/wykop-sdk-reborn',
    install_requires=requires,
    tests_require=requires + tests_requires,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
