#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import glob

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

mirror_files = glob.glob("data/mirrors/*")

setup(
    name='pacman-mirrors',
    version='20150808',
    description="Package that provides all mirrors for Manjaro Linux.",
    long_description=readme + '\n\n' + history,
    author="Roland Singer, Esclapion, philm, Ramon Buldó",
    author_email='ramon@manjaro.org',
    url='https://github.com/manjaro/pacman-mirrors',
    packages=['pacman_mirrors'],
    package_dir={'pacman_mirrors': 'pacman_mirrors'},
    data_files=[('etc', ['conf/pacman-mirrors.conf']),
                ('etc/pacman.d/mirrors', mirror_files)],
    install_requires=requirements,
    license="GPL3",
    zip_safe=False,
    keywords='pacman-mirrors',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End User/Desktop',
        'License :: OSI Approved :: GPL3 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Console'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
