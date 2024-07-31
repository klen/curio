VIRTUAL_ENV ?= .venv

all: $(VIRTUAL_ENV)

$(VIRTUAL_ENV): pyproject.toml .pre-commit-config.yaml
	@[ -d $(VIRTUAL_ENV) ] || python -m venv $(VIRTUAL_ENV)
	@$(VIRTUAL_ENV)/bin/pip install -e .[test]
	@$(VIRTUAL_ENV)/bin/pre-commit install
	@touch $(VIRTUAL_ENV)

VPART	?= minor

.PHONY: release
release: $(VIRTUAL_ENV)
	git checkout develop
	git pull
	git checkout master
	git pull
	git merge develop
	$(VIRTUAL_ENV)/bin/bump2version $(VPART)
	git checkout develop
	git merge master
	git push --tags origin develop master

.PHONY: minor
minor:
	make release VPART=minor

.PHONY: patch
patch:
	make release VPART=patch

.PHONY: major
major:
	make release VPART=major

.PHONY: clean
# target: clean - Display callable targets
clean:
	rm -rf build/ dist/ docs/_build *.egg-info $(PACKAGE)/*.c $(PACKAGE)/*.so $(PACKAGE)/*.html
	find $(CURDIR) -name "*.py[co]" -delete
	find $(CURDIR) -name "*.orig" -delete
	find $(CURDIR) -name "__pycache__" | xargs rm -rf

mypy: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/mypy

ruff: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/ruff check --fix curio

test t: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/pytest -v
