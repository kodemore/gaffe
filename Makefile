dir_src = gaffe
dir_tests = tests
.DEFAULT_GOAL := all

toml_sort:
	toml-sort pyproject.toml --all --in-place

isort:
	poetry run isort $(dir_src) $(dir_tests)

black:
	poetry run black -S -l 120 --target-version py38 $(dir_src) $(dir_tests)

mypy:
	poetry run mypy --install-types --show-error-codes --non-interactive $(dir_src)

test:
	poetry run pytest $(dir_tests)

lint: isort black mypy

tests: test

all: lint tests
