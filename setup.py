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

mirror_files = glob.glob('data/mirrors/*')

setup(
    name='pacman-mirrors',
    version='2.0',
    description="Package that provides all mirrors for Manjaro Linux.",
    long_description=readme + '\n\n' + history,
    author="Roland Singer, Esclapion, philm, Ramon Buldó",
    author_email='ramon@manjaro.org',
    url='https://github.com/manjaro/pacman-mirrors',
    packages=['pacman_mirrors'],
    package_dir={'pacman_mirrors': 'pacman_mirrors'},
    data_files=[('/etc', ['conf/pacman-mirrors.conf']),
                ('/etc/pacman.d/mirrors', mirror_files),
                ('share/locale/ca/LC_MESSAGES', ['locale/ca/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/cs/LC_MESSAGES', ['locale/cs/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/cy/LC_MESSAGES', ['locale/cy/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/de/LC_MESSAGES', ['locale/de/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/es/LC_MESSAGES', ['locale/es/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/es_419/LC_MESSAGES', ['locale/es_419/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/fr/LC_MESSAGES', ['locale/fr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/is/LC_MESSAGES', ['locale/is/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/is_IS/LC_MESSAGES', ['locale/is_IS/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/it/LC_MESSAGES', ['locale/it/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/sv/LC_MESSAGES', ['locale/sv/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/tr/LC_MESSAGES', ['locale/tr/LC_MESSAGES/pacman_mirrors.mo'])
                ('share/locale/tr_TR/LC_MESSAGES', ['locale/tr_TR/LC_MESSAGES/pacman_mirrors.mo']),],
    scripts=["scripts/pacman-mirrors"],
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
        'Programming Language :: Python :: 3.5',
        'Environment :: Console'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
