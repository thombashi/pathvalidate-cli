PYTHON := python3

FIRST_RELEASE_YEAR := 2023
LAST_UPDATE_YEAR := $(shell git log -1 --format=%cd --date=format:%Y)


.PHONY: build
build: clean
	$(PYTHON) -m tox -e build
	ls -lh dist/*

.PHONY: check
check:
	$(PYTHON) -m tox -e lint

.PHONY: clean
clean:
	$(PYTHON) -m tox -e clean

.PHONY: fmt
fmt:
	$(PYTHON) -m tox -e fmt

.PHONY: release
release:
	$(PYTHON) -m tox -e release
	$(MAKE) clean

.PHONY: setup-ci
setup-ci:
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade pip
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade tox

.PHONY: setup-dev
setup-dev: setup-ci
	$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade -e .[test]
	$(PYTHON) -m pip check

.PHONY: test
test:
	$(PYTHON) -m tox -e py

.PHONY: update-copyright
update-copyright:
	sed -i "s/^__copyright__ = .*/__copyright__ = f\"Copyright $(FIRST_RELEASE_YEAR)-$(LAST_UPDATE_YEAR), {__author__}\"/" pathvalidate_cli/__version__.py
	sed -i "s/^Copyright (c) .* Tsuyoshi Hombashi/Copyright (c) $(FIRST_RELEASE_YEAR)-$(LAST_UPDATE_YEAR) Tsuyoshi Hombashi/" LICENSE
