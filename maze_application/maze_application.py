from collections.abc import Iterator
from typing import Any
from maze_generator.helpers import create_closed_maze
from maze_generator.models import Cell
from maze_generator.generator import MazeGenerator
from maze_output import MazeOutput
from maze_renderer import MazeRenderer


class MazeApplication:
    """Coordinate maze generation, output and rendering."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the maze application."""
        self.config = config

        self.generator = MazeGenerator(
            config["WIDTH"],
            config["HEIGHT"],
            config["ENTRY"],
            config["EXIT"],
            config["SEED"],
        )

        self.maze: list[list[Cell]] = []
        self.solution: list[tuple[int, int]] = []
        self.renderer: MazeRenderer | None = None

    def run(self) -> None:
        """Generate, save and display the initial maze."""
        self.maze = self._build_maze()

        self._write_output()

        self.renderer = MazeRenderer(
            maze=self.maze,
            entry=self.config["ENTRY"],
            exit=self.config["EXIT"],
            solution=self.solution,
            regenerate_callback=self.regenerate_maze,
        )

        self.renderer.run()

    def _build_maze(self) -> list[list[Cell]]:
        """Generate a complete maze according to the configuration.

        Returns:
            The generated maze.
        """
        if self.config["PERFECT"]:
            maze = self.generator.generate_perfect()
        else:
            maze = self.generator.generate_no_perfect()

        self.solution = MazeGenerator.find_path(
            maze,
            self.generator.entry,
            self.generator.exit,
        )

        return maze

    def _write_output(self) -> bool:
        """Write the current maze and solution to the output file.

        Returns:
            True if the output was successfully written.
        """
        output = MazeOutput(
            maze=self.maze,
            entry=self.config["ENTRY"],
            exit=self.config["EXIT"],
            output_file=self.config["OUTPUT_FILE"],
        )

        return output.write(self.solution)

    def _generate_steps(
        self,
        maze: list[list[Cell]],
    ) -> Iterator[list[list[Cell]]]:
        """Generate the steps used to animate maze creation.

        Args:
            maze: Maze being generated.

        Yields:
            Intermediate maze states.
        """
        yield from self.generator.generate_steps(maze)

        if not self.config["PERFECT"]:
            yield self.generator.generate_no_perfect(maze)

        self.maze = maze

        self.solution = MazeGenerator.find_path(
            maze,
            self.generator.entry,
            self.generator.exit,
        )
        self._write_output()

    def regenerate_maze(
        self,
    ) -> tuple[list[list[Cell]], list[tuple[int, int]]]:
        """Create a new maze and start its generation animation.

        Returns:
            The initial closed maze and an empty solution.
        """
        shared_maze = create_closed_maze(
            self.config["WIDTH"],
            self.config["HEIGHT"],
        )

        if self.renderer is not None:
            self.renderer.start_generation(
                self._generate_steps(shared_maze)
            )

        return shared_maze, []
