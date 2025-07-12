# Financial Data Fetcher Makefile

.PHONY: install install-dev test test-cov clean build upload format lint type-check help

help:
	@echo "Financial Data Fetcher - Available commands:"
	@echo "  install       Install production dependencies"
	@echo "  install-dev   Install development dependencies"
	@echo "  test          Run tests"
	@echo "  test-cov      Run tests with coverage"
	@echo "  clean         Clean up cache and build artifacts"
	@echo "  build         Build the package"
	@echo "  upload        Upload to PyPI"
	@echo "  format        Format code with black"
	@echo "  lint          Run linting checks"
	@echo "  type-check    Run type checking"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ -v --cov=financial_data_fetcher --cov-report=html

clean:
	python scripts/clean.py

build:
	python -m build

upload:
	python -m twine upload dist/*

format:
	python -m black .
	python -m isort .

lint:
	python -m flake8 .

type-check:
	python -m mypy src/financial_data_fetcher/

demo:
	python scripts/example.py

dashboard:
	python -m financial_data_fetcher.dashboard

scheduler:
	python -m financial_data_fetcher.scheduler

all: clean install-dev format lint type-check test build
