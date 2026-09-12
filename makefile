PYTHON = python3
VENV = .venv
BIN = $(VENV)/bin

MLX = ./mlx-2.4-py3-none-any.whl

install:
	@test -f "$(MLX)" || { echo "ERROR: $(MLX) does not exist"; exit 1; }
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt
	$(BIN)/pip install "$(MLX)"
run:
	$(BIN)/python a_maze_ing.py config.txt

debug:
	$(BIN)/python -m pdb a_maze_ing.py config.txt

lint:
	$(BIN)/flake8 .
	$(BIN)/mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(BIN)/flake8 . && $(BIN)/mypy . --strict

build:
	$(BIN)/python -m build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build dist

.PHONY: install run debug lint build clean
