PROJECT_NAME = spideroptic-cli
SHELL := /bin/sh
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  all                      to setup the whole development environment for the project"
	@echo "  virtualenv               to create the virtualenv for the project"
	@echo "  test                     run tests"
	@echo "  docker                   docker build"
	@echo "  dist                     create build"
	@echo "  dist-upload              upload to pypi"

.PHONY: clean virtualenv test docker dist dist-upload

all: clean virtualenv

clean:
	find . -name '*.py[co]' -delete

virtualenv:
	virtualenv --python=python3 --prompt '|> spideroptic <| ' env
	env/bin/pip install -r requirements-dev.txt
	env/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

test:
	python -m pytest \
		-v \
		--cov=spideroptic \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t spideroptic:latest .

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
