#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

from opps import infographics


install_requires = ["opps", "jsonfield"]

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Framework :: Django",
               'Programming Language :: Python',
               "Programming Language :: Python :: 2.7",
               "Operating System :: OS Independent",
               "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
               'Topic :: Software Development :: Libraries :: Python Modules']

try:
    long_description = open('README.md').read()
except:
    long_description = infographics.__description__

setup(name='opps-infographics',
        namespace_packages=['opps', 'opps.infographics'],
        version=infographics.__version__,
        description=infographics.__description__,
        long_description=long_description,
        classifiers=classifiers,
        keywords='infographic opps cms django apps magazines websites',
        author=infographics.__author__,
        author_email=infographics.__email__,
        url='http://oppsproject.org',
        download_url="https://github.com/YACOWS/opps-infographics/tarball/master",
        license=infographics.__license__,
        packages=find_packages(exclude=('doc', 'docs',)),
        package_dir={'opps': 'opps'},
        install_requires=install_requires,
        include_package_data=True,
        package_data={
           'infographics': ['templates/*']
        })
