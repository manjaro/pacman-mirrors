#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import io
import re
import os

from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

mirror_files = glob.glob('data/mirrors/*')

setup(
    name='pacman-mirrors',
    version=find_version("pacman_mirrors", "__init__.py"),
    description="Package that provides all mirrors for Manjaro Linux.",
    long_description=readme + '\n\n' + changelog,
    author="Roland Singer, Esclapion, philm, Ramon Buldó",
    author_email='ramon@manjaro.org',
    url='https://github.com/manjaro/pacman-mirrors',
    packages=['pacman_mirrors'],
    package_dir={'pacman_mirrors': 'pacman_mirrors'},
    data_files=[('/etc', ['conf/pacman-mirrors.conf']),
                ('/etc/pacman.d/mirrors', mirror_files),
                ('share/locale/bg/LC_MESSAGES', ['locale/bg/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/ca/LC_MESSAGES', ['locale/ca/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/cs/LC_MESSAGES', ['locale/cs/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/cy/LC_MESSAGES', ['locale/cy/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/da/LC_MESSAGES', ['locale/da/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/de/LC_MESSAGES', ['locale/de/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/el/LC_MESSAGES', ['locale/el/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/es/LC_MESSAGES', ['locale/es/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/es_419/LC_MESSAGES', ['locale/es_419/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/fr/LC_MESSAGES', ['locale/fr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/hr/LC_MESSAGES', ['locale/hr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/is/LC_MESSAGES', ['locale/is/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/is_IS/LC_MESSAGES', ['locale/is_IS/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/it/LC_MESSAGES', ['locale/it/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/lt/LC_MESSAGES', ['locale/lt/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/pl/LC_MESSAGES', ['locale/pl/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/ru_RU/LC_MESSAGES', ['locale/ru_RU/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/sk/LC_MESSAGES', ['locale/sk/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/sv/LC_MESSAGES', ['locale/sv/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/tr/LC_MESSAGES', ['locale/tr/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/tr_TR/LC_MESSAGES', ['locale/tr_TR/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/uk/LC_MESSAGES', ['locale/uk/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/uk_UA/LC_MESSAGES', ['locale/uk_UA/LC_MESSAGES/pacman_mirrors.mo']),
                ('share/locale/zh_TW/LC_MESSAGES', ['locale/zh_TW/LC_MESSAGES/pacman_mirrors.mo']),
                ],
    scripts=["scripts/pacman-mirrors"],
    install_requires=requirements,
    license="GPL3",
    zip_safe=False,
    keywords='pacman-mirrors',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End User/Desktop',
        'License :: OSI Approved :: GPL3 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
