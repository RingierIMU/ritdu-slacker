MODULES = ritdu_slacker tests

help:
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build the package
	poetry build

check: ## Check the package
	twine check --strict dist/*

clean: ## Clean the package
	rm -rf dist/*

install-dev: install vscode ## Setup development environment

format: ## Format the code
	poetry run black $(MODULES)

install: ## Install all dependencies
	poetry install --sync

install-prod: ## Install production dependencies
	poetry install --without=dev --sync

lint: ## Lint the code
	poetry run black --check $(MODULES)
	-poetry run pylint $(MODULES)

lock: ## Update dependency lockfile
	poetry lock

publish: install-prod clean build check ## Publish the package
	poetry publish

publish-test: install clean build check ## Publish to the package to the PyPI test platform
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish --repository testpypi

setup-dev: setup-binaries install-dev vscode

setup-binaries: ## Setup binaries for development. Poetry, Twine.
	brew install pipx || python3 -m pip install --user pipx
	pipx ensurepath
	pipx install poetry
	pipx install twine

test: ## Test the package
	poetry run pytest

vscode: ## Update VSCode settings
	@[ -d .vscode ] \
		&& echo "{\"python.defaultInterpreterPath\": \"$(shell which python)\", \"python.terminal.activateEnvInCurrentTerminal\": true}" > .vscode/settings.json \
		|| exit 0
