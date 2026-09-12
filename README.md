*This project has been created as part of the 42 curriculum by aluzardo, masalomo.*

## Description

A‑Maze‑ing is a Python 3.10+ project that generates mazes — either **perfect** (a single path between entry and exit) or **imperfect** (a Pac‑Man‑style board with multiple routes). The generator is implemented as a reusable `MazeGenerator` class that can be installed as a pip package (`mazegen`). A graphical renderer built on the 42 MiniLibX (MLX CLXV) library displays the maze with colour‑coded walls, the “42” logo, and interactive controls (regenerate, show path, change colours, etc.). The project also writes the maze to a text file using a hexadecimal wall encoding.

## Instructions

### Prerequisites
- **MLX CLXV** (MiniLibX) – required for the graphical renderer.
- **Python 3.10** or newer.
- **Git**.

### Installing the project
```bash
make install
```
Make install will:
    - create a virtual environment
    - install Python dependencies
    - install the maze mlx library


### Running the application
```bash
# using the Makefile
make run

# directly with Python (the config file is required)
python3 a_maze_ing.py config.txt
```

### Available Commands (Makefile)
```bash
make install    # install dependencies (creates virtualenv, installs requirements, installs MLX)
make build      # build the distributable wheel (produces mazegen-*.whl)
make run        # start the graphical application
make debug      # run with pdb
make lint       # flake8 + mypy
make lint‑strict # stricter mypy checks
make clean      # remove caches and compiled files
```


## Configuration file

The project reads a simple `KEY=VALUE` text file (see `config.txt`). All keys are case‑sensitive and comments start with `#`.

| Key               | Description                                   | Example                     |
|-------------------|-----------------------------------------------|-----------------------------|
| `WIDTH`           | Maze width (number of cells)                  | `WIDTH=20`                  |
| `HEIGHT`          | Maze height (number of cells)                 | `HEIGHT=20`                 |
| `ENTRY`           | Entry coordinates `x,y` (zero‑based)          | `ENTRY=0,0`                 |
| `EXIT`            | Exit coordinates `x,y`                        | `EXIT=19,19`                |
| `OUTPUT_FILE`     | File to which the maze is written             | `OUTPUT_FILE=maze.txt`      |
| `PERFECT`         | `True` for a perfect maze, `False` otherwise  | `PERFECT=False`             |
| `SEED`            | Optional seed for reproducibility (string)    | `SEED=12345`                |


## Algorithm

The generator uses two stages:

1. **Perfect maze generation** – a depth‑first recursive‑backtracking algorithm (also called *recursive backtracker*). It carves passages by maintaining a stack of cells, selecting a random neighbour, removing the wall, and back‑tracking when a dead end is reached. The implementation lives in `maze_generator/perfect.py`.

2. **Imperfect maze conversion** – after a perfect maze is built, the `imperfect.py` module removes a subset of dead‑end walls to create loops, ensuring the board is *playable* (multiple routes) while still keeping the “42” logo intact.

The algorithm also inserts the “42” logo by forcing a pattern of closed cells (`generate_42logo` in `helpers.py`).

## Why this algorithm?

- **Deterministic with a seed** – the same seed always yields the same maze, which is required by the project specifications.
- **Simple and well‑studied** – recursive backtracking guarantees a perfect maze (single unique solution) and is easy to implement and debug.
- **Extensible** – the post‑processing step allows us to create the imperfect, Pac‑Man‑style boards required for the “default” mode.
- **Performance** – the algorithm runs in O(N) time for an N‑cell maze, fast enough for interactive generation even on modest hardware.

## Reusability

The core generator is packaged as a standalone module (`mazegen`) that can be installed with `pip`. The public API consists of the `MazeGenerator` class and the static method `find_path`.

```python
from maze_generator.generator import MazeGenerator

# initialise the generator
gen = MazeGenerator(
    width=20,
    height=20,
    entry=(0, 0),           # (x, y)
    exit=(19, 19),
    seed="42seed"
)

# generate a perfect maze
maze = gen.generate_perfect()

# obtain the solution path
solution = MazeGenerator.find_path(
    maze,
    entry=(0, 0),
    exit=(19, 19)
)

# `maze` is a list of lists of `Cell` objects; `solution` is a list of
# (row, col) tuples.
```

The package can be reused in other projects by importing the class as shown above, or by installing the wheel (`mazegen-*.whl`) and using the CLI entry point `maze_generator`.

## Team & Project Management

| Member | Role |
|--------|------|
| **aluzardo** (Alejandro Luzardo) | Project coordination, core engine, documentation, packaging, code‑review. |
| **masalomo** (Manuel Salomone) | Graphics & UI – MiniLibX renderer, parser, interactive controls, git workflow, code‑review. |

### Planning & Evolution
1. **Initial prototype** – implemented `MazeGenerator` with a perfect‑maze recursive backtracker and a simple CLI.
2. **Configuration parser** – added `config_parser.py` using Pydantic for robust validation (commit `101ef8c`).
3. **Graphical renderer** – integrated MiniLibX with interactive keyboard shortcuts (commits `0e86ad1`, `c2243a7`).
4. **Imperfect mode** – post‑processing to remove dead ends and add loops (commit `a6611e5`).
5. **Packaging** – created a pip‑installable wheel (`mazegen-1.0.0-py3-none-any.whl`) and added Makefile targets (commit `a165c2f`).
6. **Linting** – introduced `flake8`, `mypy` and strict lint rule (`lint‑strict`) (commit `63ecfe6`).

### What worked well
- **Modular design** – generator, renderer and configuration are clearly separated, making the core reusable.
- **Continuous integration** – automated linting and type checking catch regressions early.

### What didn't
- **Chosing MLX** - we love complicating our lives

### Areas for improvement
- **More algorithms** – exposing additional generation strategies (Prim, Kruskal) would make the library more versatile.

### Tools used
- **Version control:** Git
- **Build system:** Make, setuptools (`setup.cfg`/`pyproject.toml`)
- **Language:** Python 3.10+, type hints, Pydantic
- **Linters:** flake8, mypy
- **Graphics:** MiniLibX CLXV
- **Claude Code** – used for documentation and review complicated concepts.


## Resources

- **MLX CLXV repository** – https://github.com/42school/mlx_CLXV
- **Recursive backtracker algorithm** – https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker
- **PEP 8 – Style Guide for Python Code** – https://peps.python.org/pep-0008/
- **Mypy – Optional static typing for Python** – https://mypy.readthedocs.io/

## License

The project is released under the **MIT License**
Copyright © 2026 Alejandro Luzardo, Manuel Salomone.
