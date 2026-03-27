.PHONY: help install dev test lint typecheck paper clean docker-build docker-run

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package
	pip install -e .

dev:  ## Install with all dev dependencies
	pip install -e ".[all]"
	pre-commit install

test:  ## Run test suite
	pytest tests/ -v

test-fast:  ## Run tests excluding slow/fenics
	pytest tests/ -v -m "not slow and not fenics"

lint:  ## Run linter
	ruff check src/ tests/ scripts/
	ruff format --check src/ tests/ scripts/

format:  ## Auto-format code
	ruff check --fix src/ tests/ scripts/
	ruff format src/ tests/ scripts/

typecheck:  ## Run type checker
	mypy src/browntone/

paper:  ## Build LaTeX paper
	cd paper && latexmk -pdf -interaction=nonstopmode main.tex

paper-clean:  ## Clean LaTeX build artifacts
	cd paper && latexmk -C

docker-build:  ## Build Docker image
	docker build -f docker/Dockerfile -t browntone:latest .

docker-run:  ## Run interactive Docker container
	docker compose -f docker/docker-compose.yml run --rm browntone bash

clean:  ## Remove build artifacts
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
