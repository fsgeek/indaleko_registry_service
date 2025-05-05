# Makefile for indaleko_registry_service

.PHONY: run test lint clean dev

UV ?= uv
PYTHON ?= python3

run:
	@echo "Starting registry service on http://localhost:8000 ..."
	@$(PYTHON) -m uvicorn src.indaleko_registry_service.registry_service:app --reload

test:
	@echo "Running tests..."
	@$(UV) pip install -e .[dev] > /dev/null
	@pytest

lint:
	@echo "Running ruff linting..."
	@$(UV) pip install ruff > /dev/null
	ruff check src/ tests/

clean:
	@echo "Cleaning up..."
	rm -rf .pytest_cache
	rm -rf dist build *.egg-info
	find . -name "__pycache__" -type d -exec rm -r {} +

dev:
	@echo "Installing development environment..."
	@$(UV) pip install -e .[dev]
	@$(UV) pip install ruff
	@$(UV) pip install pytest
	@$(UV) pip install pytest-cov
