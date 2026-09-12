from maze_generator.models import Cell, CellStatus

from .image import MlxImage


class MazeDrawer:
    """Draw maze elements using a MiniLibX image."""

    def __init__(
        self,
        image: MlxImage,
        cell_size: int,
        maze_width: int,
        maze_height: int,
    ) -> None:
        """Initialize the maze drawer.

        Args:
            image: Image used for drawing.
            cell_size: Size of each maze cell in pixels.
            maze_width: Number of cells horizontally.
            maze_height: Number of cells vertically.
        """
        self.image: MlxImage = image
        self.cell_size: int = cell_size
        self.maze_width: int = maze_width
        self.maze_height: int = maze_height

    def draw_maze(
        self,
        maze: list[list[Cell]],
        solution: list[tuple[int, int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        show_path: bool,
        path_color: int,
        logo_color: int,
        entry_color: int,
        exit_color: int,
        wall_color: int,
    ) -> None:
        """Draw the complete maze.

        Args:
            maze: Two-dimensional maze structure.
            solution: Shortest path as (row, column) coordinates.
            entry: Entry position as (x, y).
            exit: Exit position as (x, y).
            show_path: Whether to display the solution.
            path_color: Color of the solution path.
            logo_color: Color of the 42 logo.
            entry_color: Color of the entry cell.
            exit_color: Color of the exit cell.
            wall_color: Color of the maze walls.
        """
        if show_path:
            self.draw_solution(solution, entry, exit, path_color)

        self.draw_logo(maze, logo_color)
        self.draw_cell(*entry, entry_color)
        self.draw_cell(*exit, exit_color)
        self.draw_walls(maze, wall_color)

    def draw_walls(self, maze: list[list[Cell]], color: int) -> None:
        """Draw all walls in the maze.

        Args:
            maze: Two-dimensional maze structure.
            color: Wall color.
        """
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                px: int = x * self.cell_size
                py: int = y * self.cell_size
                size: int = self.cell_size

                if cell.north:
                    self._horizontal_line(px, py, size, color)

                if cell.east:
                    self._vertical_line(px + size - 1, py, size, color)

                if cell.south:
                    self._horizontal_line(px, py + size - 1, size, color)

                if cell.west:
                    self._vertical_line(px, py, size, color)

    def draw_cell(self, x: int, y: int, color: int) -> None:
        """Draw a colored cell.

        Args:
            x: Horizontal cell coordinate.
            y: Vertical cell coordinate.
            color: Cell color.
        """
        if not self._valid_cell(x, y):
            return

        padding: int = max(3, self.cell_size // 4)
        size: int = self.cell_size - 2 * padding

        start_x: int = x * self.cell_size + padding
        start_y: int = y * self.cell_size + padding

        for py in range(start_y, start_y + size):
            for px in range(start_x, start_x + size):
                self.image.draw_pixel(px, py, color)

    def draw_logo(self, maze: list[list[Cell]], color: int) -> None:
        """Draw cells belonging to the 42 logo.

        Args:
            maze: Two-dimensional maze structure.
            color: Logo color.
        """
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell.status == CellStatus.LOGO:
                    self.draw_cell(x, y, color)

    def draw_solution(
        self,
        solution: list[tuple[int, int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        color: int,
    ) -> None:
        """Draw the shortest path between entry and exit.

        MazeGenerator returns coordinates as (row, column),
        while MazeDrawer uses (x, y).

        Args:
            solution: Path represented as (row, column) coordinates.
            entry: Entry position as (x, y).
            exit: Exit position as (x, y).
            color: Path color.
        """
        for row, col in solution:
            point: tuple[int, int] = (col, row)

            if point == entry or point == exit:
                continue

            self.draw_cell(col, row, color)

    def _horizontal_line(
        self,
        x: int,
        y: int,
        length: int,
        color: int,
    ) -> None:
        """Draw a horizontal line.

        Args:
            x: Starting horizontal coordinate.
            y: Vertical coordinate.
            length: Line length in pixels.
            color: Line color.
        """
        for i in range(length):
            self.image.draw_pixel(x + i, y, color)

    def _vertical_line(
        self,
        x: int,
        y: int,
        length: int,
        color: int,
    ) -> None:
        """Draw a vertical line.

        Args:
            x: Horizontal coordinate.
            y: Starting vertical coordinate.
            length: Line length in pixels.
            color: Line color.
        """
        for i in range(length):
            self.image.draw_pixel(x, y + i, color)

    def _valid_cell(self, x: int, y: int) -> bool:
        """Check whether a cell coordinate is inside the maze.

        Args:
            x: Horizontal cell coordinate.
            y: Vertical cell coordinate.

        Returns:
            True if the coordinates are inside the maze.
        """
        return (0 <= x < self.maze_width and 0 <= y < self.maze_height)
