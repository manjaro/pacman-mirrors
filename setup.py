#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

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

setup(
    name='pacman-mirrors',
    version='20150808',
    description="Package that provides all mirrors for Manjaro Linux.",
    long_description=readme + '\n\n' + history,
    author="Roland Singer, Esclapion, philm, Ramon Buldó",
    author_email='ramon@manjaro.org',
    url='https://github.com/manjaro/pacman-mirrors',
    packages=[
        'pacman_mirrors',
        'pacman_mirrors_gui'
    ],
    package_dir={'pacman_mirrors':
                 'pacman_mirrors',
                 'pacman_mirrors_gui':
                 'pacman_mirrors'},
    include_package_data=True,
    data_files=[('/etc', ['conf/pacman-mirrors-conf'])],
    install_requires=requirements,
    license="GPL3",
    zip_safe=False,
    keywords='pacman-mirrors',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL3 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
