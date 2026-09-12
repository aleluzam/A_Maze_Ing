from typing import Iterator
from .models import Cell, MazeError
from .helpers import (
    create_closed_maze,
    inside,
    bfs,
    reconstruct_path
)
from .perfect import (
    generate_perfect_maze_steps,
    generate_perfect_maze,
)
from .imperfect import generate_no_perfect_maze

__all__ = ["Cell", "create_closed_maze"]


class MazeGenerator:
    """Reusable maze generator.

    Provides methods to create perfect mazes (single unique path) and to
    transform them into imperfect mazes with loops. The generator also
    offers a static method to find the shortest path between two cells.

    Example:
        >>> gen = MazeGenerator(width=20, height=15,
        ...                     entry=(0, 0), exit=(19, 14), seed="42")
        >>> maze = gen.generate_perfect()
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: str | None,
    ) -> None:
        """Initialize the generator with size, entry/exit, and optional seed.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
            entry: (x, y) coordinates of the entry cell.
            exit: (x, y) coordinates of the exit cell.
            seed: Optional seed for deterministic generation; ``None`` yields a
                fully random maze.

        The constructor converts the public (x, y) coordinates to internal
        (row, column) representation used by the generator.
        """
        try:
            self.width = width
            self.height = height
            # Convert to internal (row, col) coordinates
            self.entry = (entry[1], entry[0])
            self.exit = (exit[1], exit[0])
            self.seed = seed
        except Exception as e:
            raise MazeError("invalid generator parameters") from e

    def generate_perfect(self) -> list[list[Cell]]:
        """Generate a perfect maze and return a grid of :class:`Cell` objects.

        Returns:
            A two‑dimensional list representing the maze where each element
            is a :class:`Cell` with wall information.
        """
        try:
            maze = create_closed_maze(self.width, self.height)
            maze = generate_perfect_maze(
                maze,
                self.entry,
                self.exit,
                self.seed,
            )
            return maze
        except Exception as e:
            raise MazeError("failed to generate perfect maze") from e

    def generate_steps(
        self,
        maze: list[list[Cell]] | None = None,
    ) -> Iterator[list[list[Cell]]]:
        """Yield the maze after each generation step.

        Args:
            maze: Optional pre‑created maze grid; if omitted a closed maze is
                created automatically.

        Yields:
            The maze grid after each step of the recursive‑backtracker
            algorithm.
        """
        try:
            if maze is None:
                maze = create_closed_maze(self.width, self.height)
            yield from generate_perfect_maze_steps(
                maze,
                self.entry,
                self.exit,
                self.seed,
            )
        except Exception as e:
            raise MazeError("failed to generate steps") from e

    def generate_no_perfect(
        self,
        maze: list[list[Cell]] | None = None,
    ) -> list[list[Cell]]:
        """Create an imperfect maze from a perfect one.

        The method first generates a perfect maze and then applies the
        imperfect conversion algorithm which opens selected walls to introduce
        loops while preserving the 42 logo.

        Args:
            maze: Optional pre‑created maze; when ``None`` a closed maze is
                allocated automatically.

        Returns:
            The resulting imperfect maze as a grid of :class:`Cell` objects.
        """
        try:
            if maze is None:
                maze = create_closed_maze(self.width, self.height)
            # First generate a perfect maze
            maze = generate_perfect_maze(
                maze,
                self.entry,
                self.exit,
                self.seed,
            )
            maze = generate_no_perfect_maze(
                maze,
                self.seed
            )
            return maze
        except Exception as e:
            raise MazeError("failed to generate imperfect maze") from e

    @staticmethod
    def find_path(
        maze: list[list[Cell]],
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Find the shortest path from entry to exit.

        Expects entry and exit as (row, col) coordinates.
        Returns a list of (row, col) coordinates forming the path.
        """
        if not maze or not maze[0]:
            return []
        rows = len(maze)
        cols = len(maze[0])

        if not inside(entry, rows, cols) or not inside(exit, rows, cols):
            return []

        parents = bfs(maze, entry, exit, rows, cols)
        return reconstruct_path(parents, exit)
