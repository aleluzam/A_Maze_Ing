"""Utilities for writing generated mazes to the required output format."""

from pathlib import Path
from typing import Sequence
from maze_generator.models import Cell


Coordinate = tuple[int, int]


class MazeOutput:
    """Serialize a generated maze into the A-Maze-Ing output format."""

    def __init__(
        self,
        maze: Sequence[Sequence[Cell]],
        entry: Coordinate,
        exit: Coordinate,
        output_file: str,
    ) -> None:
        """Initialize the maze output writer.

        Args:
            maze: Generated maze containing Cell objects.
            entry: Entry coordinates as (x, y).
            exit: Exit coordinates as (x, y).
            output_file: Destination output file.
        """
        self.maze = maze
        self.entry = entry
        self.exit = exit
        self.output_file = output_file

    def _maze_lines(self) -> list[str]:
        """Convert the maze to hexadecimal rows.

        Returns:
            One hexadecimal string for every maze row.
        """
        return [
            "".join(cell.to_hex() for cell in row)
            for row in self.maze
        ]

    @staticmethod
    def path_to_directions(
        path: Sequence[Coordinate],
    ) -> str:
        """Convert a coordinate path to N/E/S/W directions.

        Args:
            path: Ordered (row, col) coordinates forming a path.

        Returns:
            The path represented as N, E, S and W characters.

        Raises:
            ValueError: If two consecutive cells are not adjacent.
        """
        directions: dict[tuple[int, int], str] = {
            (-1, 0): "N",  # d_row = -1 (North)
            (0, 1): "E",   # d_col = 1  (East)
            (1, 0): "S",   # d_row = 1  (South)
            (0, -1): "W",  # d_col = -1 (West)
        }

        result: list[str] = []

        for current, next_cell in zip(path, path[1:]):
            d_row = next_cell[0] - current[0]
            d_col = next_cell[1] - current[1]

            direction = directions.get((d_row, d_col))

            if direction is None:
                raise ValueError(
                    f"Invalid path step: {current} -> {next_cell}"
                )

            result.append(direction)

        return "".join(result)

    def write(self, solution: Sequence[Coordinate]) -> bool:
        """Write the maze, entry, exit and solution to a file.

        Args:
            solution: Shortest path from entry to exit.

        Returns:
            True if the file was written successfully, otherwise False.
        """
        try:
            lines = self._maze_lines()

            lines.extend(
                [
                    "",
                    f"{self.entry[0]},{self.entry[1]}",
                    f"{self.exit[0]},{self.exit[1]}",
                    self.path_to_directions(solution),
                ]
            )

            content = "\n".join(lines) + "\n"

            with Path(self.output_file).open(
                "w",
                encoding="utf-8",
            ) as output_file:
                output_file.write(content)

            return True

        except (OSError, ValueError, TypeError) as error:
            print(
                f"Error: could not write maze output "
                f"'{self.output_file}': {error}"
            )
            return False
