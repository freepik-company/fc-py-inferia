.PHONY: all help help-variables install dist upload clean

PYTHON_VERSION ?= 3.10
REPOSITORY?=testpypi


all: help

help: help-variables  ## Autogenerated list of commands
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

help-variables:
	@echo "Variables:"
	@echo "  PYTHON_VERSION: $(PYTHON_VERSION)"
	@echo "  REPOSITORY: $(REPOSITORY)"

##@ Development commands

check-utils: check-uv check-twine ## Check the required utilities

check-uv:
	@uv version || (echo "Please install uv using: make build-install-uv" && exit 1)

check-twine:
	@twine --version || (echo "Please install twine using: make build-install-twine" && exit 1)

.venv: check-uv ## Create the virtual environment
	@uv venv --python $(PYTHON_VERSION)

build: .venv dependencies-install ## Build the local development environment

git-prune: ## Prune the git repository
	@git branch --format '%(refname:short) %(upstream:track)' | \
		grep -E '\[gone\]|\[desaparecido\]' | \
		awk '{print $$1}' > .branches_to_delete
	@vim .branches_to_delete
	@if [ -s .branches_to_delete ]; then \
		echo "Deleting selected branches..."; \
		cat .branches_to_delete | xargs -I {} git branch -D {}; \
	else \
		echo "No branches were selected for deletion."; \
	fi
	@rm .branches_to_delete

dependencies-compile: ## Compile the dependencies
	@. .venv/bin/activate && uv pip compile --universal -o requirements.txt --no-deps --no-annotate --no-header pyproject.toml

dependencies-install: ## Install the dependencies
	@. .venv/bin/activate && uv sync

code-style-check: ## Checks the code style.
	@. .venv/bin/activate && black --check .

code-style-dirty: ## Fixes the code style but does not commit the changes
	@. .venv/bin/activate && black .

code-style: code-style-dirty ## Check the code style and commit the changes
	@git commit -am "style: fix code style"

dev-dependencies: ## Install the development dependencies
	@. .venv/bin/activate && uv pip install -e .
	@. .venv/bin/activate && uv sync --dev

dev-build: .venv dev-dependencies ## Build the development environment
	echo "Development environment built"

run-test: dev-dependencies ## Run the tests
	@. .venv/bin/activate && python -m pytest

##@ PyPi commands

install: setup.py ## Install the package
	pip install -e .

dist: ## Build the distribution
	python -m build

upload: dist ## Upload the distribution
	twine upload \
		--repository ${REPOSITORY} \
		dist/*

##@ Clean commands
clean: ## Clean the project
	rm -rf dist build *.egg-info
