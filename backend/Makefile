.PHONY: install lint format type-check test clean run dev

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

lint:
	ruff check .

format:
	ruff format .

type-check:
	mypy .

test:
	pytest

all-checks: lint type-check test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

run:
	python main.py

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000
