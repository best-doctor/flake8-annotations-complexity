.PHONY: install test coverage types style format readme audit check

install:
	uv sync

test:
	uv run pytest

coverage:
	uv run pytest --cov=flake8_annotations_complexity --cov-report=xml --cov-report=term

types:
	uv run mypy flake8_annotations_complexity

style:
	uv run ruff check .
	uv run ruff format --check .
	uv run flake8 .

format:
	uv run ruff check --fix .
	uv run ruff format .

readme:
	npx --yes markdownlint-cli2 README.md

audit:
	uv run pip-audit

check: style types test audit
