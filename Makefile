.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate MkDocs HTML documentation, man page using Pandoc, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "pot-file - extract messages to locale/pacman_mirrors.pot"
	@echo "push-pot - push pot file to transifex"
	@echo "pull-po - pull all translations from transifex"
	@echo "mo-files - generate .mo files"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 pacman_mirrors tests

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source pacman_mirrors setup.py test
	coverage report -m
	coverage html
	firefox htmlcov/index.html

docs:
	mkdocs build
	pandoc -s -t man docs/index.md -o man/pacman-mirrors.8
	pandoc docs/index.md -f markdown -t html -s -o man/pacman-mirrors.8.html
	gzip man/pacman-mirrors.8 -fq

man-page:
	pandoc -s -t man docs/index.md -o man/pacman-mirrors.8
	man man/pacman-mirrors.8

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean mo-files
	python setup.py install --root=$(DESTDIR) --optimize=1

pot-file:
	python setup.py extract_messages --output-file locale/pacman_mirrors.pot

push-pot:
	tx push -s

pull-po:
	tx pull -a

mo-files:
	python setup.py compile_catalog --directory locale --domain pacman_mirrors
