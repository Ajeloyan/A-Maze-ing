
PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean lint lint-strict build

install:
	@poetry install

run:
	@poetry run $(PYTHON) $(SCRIPT) $(CONFIG) || true

debug:
	@poetry run $(PYTHON) -m pdb $(SCRIPT) $(CONFIG) || true

clean:
	@rm -rf */__pycache__
	@rm -rf */.mypy_cache
	@rm -rf .mypy_cache
	@rm -rf __pycache__

lint:
	@python3 -m flake8 --exclude amazevenv .
	@python3 -m mypy --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs .

lint-strict:
	@-poetry run  flake8 . --exclude .env2
	@-poetry run  mypy --strict .

build:
	@poetry build 
