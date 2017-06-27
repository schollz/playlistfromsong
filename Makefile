.PHONY: clean clean-test clean-pyc clean-build docs help

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

install: clean ## install the package to the active Python's site-packages
	python3 setup.py install --force


test:
	autopep8 --aggressive --aggressive --aggressive --in-place --recursive --max-line-length=78 playlistfromsong/__main__.py
	autopep8 --aggressive --aggressive --aggressive --in-place --recursive --max-line-length=78 playlistfromsong/server.py
	python3 setup.py test