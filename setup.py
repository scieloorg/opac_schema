#!/usr/bin/env python
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="Opac Schema",
    version='0.1',
    description="Schema of SciELO OPAC",
    author="SciELO",
    author_email="scielo@scielo.org",
    license="BSD",
    url="https://github.com/scieloorg/opac_schema",
    py_modules=['v1.models'],
    keywords='opac schema',
    maintainer_email='scielo@scielo.org',
    download_url='',
    classifiers=[],
    setup_requires=["mongoengine"],
    test_suite='tests'
)
