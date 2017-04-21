PROJECT = cli_helpers

.PHONY: clean lint lint-fix test test-all coverage docs dist release

help:
	@echo "clean - remove all build artifacts"
	@echo "lint - check code changes against PEP 8"
	@echo "lint-fix - automatically fix PEP 8 violations"
	@echo "test - run tests quickly with the current Python"
	@echo "test-all - run tests in all environments"
	@echo "coverage - run tests and check code coverage"
	@echo "docs - generate Sphinx HTML documentation"
	@echo "dist - make the source and binary distributions"
	@echo "release - package and upload a release"

clean:
	rm -rf build dist egg *.egg-info
	find . -name '*.py[co]' -exec rm -f {} +
	$(MAKE) -C docs clean

lint:
	pep8radius master --docformatter --error-status || ( pep8radius master --docformatter --diff; false )

lint-fix:
	pep8radius master --docformatter --in-place

test:
	coverage run --source $(PROJECT) -m py.test

test-all:
	tox

coverage: test
	coverage report

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/build/html/index.html

dist: clean
	python setup.py sdist bdist_wheel

release: clean dist
	twine upload -s dist/*
