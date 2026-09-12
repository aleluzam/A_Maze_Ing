# maze_generator/__init__.py
"""
maze_generator — reusable maze generation library.

This package generates mazes as a grid of Cell objects, either as a
perfect maze (single path, no loops) or as a playable board with loops
(Pac-Man-style, no dead-ends besides the "42" pattern).

Basic usage
-----------
    >>> from maze_generator import MazeGenerator
    >>> gen = MazeGenerator(
    ...     width=20,
    ...     height=15,
    ...     entry=(0, 0),
    ...     exit=(19, 14),
    ...     seed="42",
    ... )
    >>> maze = gen.generate_perfect()

Custom parameters
-----------------
    - width, height: int, size of the maze grid (number of cells).
    - entry, exit: tuple[int, int], (x, y) coordinates of the entry and
      exit cells.
    - seed: str | None, used to reproduce the same maze across runs.
      Pass None for a fully random maze.

Generation modes
-----------------
    - generate_perfect() -> list[list[Cell]]
        Returns a perfect maze: exactly one path between entry and exit,
        no loops at all.

    - generate_no_perfect(maze=None) -> list[list[Cell]]
        Returns a playable board (Pac-Man style): full connectivity,
        at least two independent routes, rare dead-ends.

    - generate_steps(maze=None) -> Iterator[list[list[Cell]]]
        Yields the maze state after every generation step, useful to
        animate the construction process.

Accessing the structure
------------------------
    Both generate_perfect() and generate_no_perfect() return a
    list[list[Cell]]: a 2D grid where maze[y][x] describes the walls
    of that cell. This structure is not the same format as the
    project's output file.

Accessing a solution
----------------------
    >>> path = MazeGenerator.find_path(maze, entry=(0, 0), exit=(19, 14))
    >>> path
    [(0, 0), (0, 1), (1, 1), ...]

Error handling
--------------
    All generation methods raise a MazeError on invalid parameters or
    generation failures.
"""

from .generator import MazeGenerator

__version__ = "1.0.0"
__all__ = ["MazeGenerator"]
