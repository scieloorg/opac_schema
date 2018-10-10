#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name="Opac Schema",
    version='2.48',
    description="Schema of SciELO OPAC",
    author="SciELO",
    author_email="scielo@scielo.org",
    license="BSD",
    url="https://github.com/scieloorg/opac_schema",
    packages=find_packages(),
    keywords='opac schema',
    maintainer_email='scielo@scielo.org',
    download_url='',
    classifiers=[],
    install_requires=[
        "blinker>=1.4",
        "mongoengine>=0.13.0",
        "python-slugify>=1.2.4",
        "legendarium>=2.0.1",
    ],
    tests_require=[
        "mongomock"
    ],
    dependency_links=[],
    test_suite='tests.discover_suite'
)
