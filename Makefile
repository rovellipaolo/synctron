PWD := $(shell pwd)
SYNCTRON_HOME := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Build:
.PHONY: build
build:
	@which pipenv || pip3 install pipenv
	@pipenv install --dev

.PHONY: generate-checkstyle-config
generate-checkstyle-config:
	@pipenv run pylint --generate-rcfile > .pylintrc


# Install:
.PHONY: install
install:
	sudo ln -s ${SYNCTRON_HOME}/synctron.py /usr/local/bin/synctron

.PHONY: uninstall
uninstall:
	sudo unlink /usr/local/bin/synctron

.PHONY: install-githooks
install-githooks:
	@pip3 install pre-commit
	pre-commit install

.PHONY: uninstall-githooks
uninstall-githooks:
	pre-commit uninstall


# Run:
.PHONY: run
run:
	@pipenv run python3 synctron.py


# Test:
.PHONY: test
test:
	@pipenv run python3 -m unittest

.PHONY: test-coverage
test-coverage:
	@pipenv run coverage3 run --branch --source=. --omit="tests/*" --data-file=".coverage" -m unittest
	@pipenv run coverage3 xml --data-file=".coverage" -o "coverage.xml"
	@pipenv run coverage3 report --data-file=".coverage" --show-missing

.PHONY: checkstyle
checkstyle:
	@pipenv run pycodestyle --max-line-length=120 synctron.py tests/
	@pipenv run pylint synctron.py tests/
