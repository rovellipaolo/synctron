PWD := $(shell pwd)
SYNCTRON_HOME := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))


# Build:
.PHONY: build
build:
	@pip3 install -r requirements.txt

.PHONY: generate-checkstyle-config
generate-checkstyle-config:
	pylint --generate-rcfile > .pylintrc


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
	@python3 synctron.py


# Test:
.PHONY: test
test:
	@python3 -m unittest

.PHONY: test-coverage
test-coverage:
	@coverage3 run --source=. --omit="tests/*" -m unittest
	@coverage3 report

.PHONY: checkstyle
checkstyle:
	pylint synctron.py tests/
