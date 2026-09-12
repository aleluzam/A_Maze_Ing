from typing import Callable, Iterator, Optional

from maze_generator.models import Cell
from maze_generator.generator import MazeGenerator

from .image import MlxImage
from .maze_animation import MazeAnimation
from .maze_drawer import MazeDrawer
from .maze_keyboard import MazeKeyboard
from .mlx_hooks import MlxHooks
from .mlx_window import MlxWindow
from .renderer_config import RendererConfig
from .status_bar import StatusBar


class MazeRenderer:
    """Display a maze using MiniLibX."""

    KEY_ESC: int = 65307
    KEY_R: int = ord("r")
    KEY_P: int = ord("p")
    KEY_C: int = ord("c")
    KEY_B: int = ord("b")
    KEY_E: int = ord("e")
    KEY_X: int = ord("x")
    KEY_S: int = ord("s")
    KEY_D: int = ord("d")
    KEY_V: int = ord("v")
    KEY_L: int = ord("l")

    def __init__(
        self,
        maze: list[list[Cell]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        solution: list[tuple[int, int]],
        regenerate_callback: Optional[
            Callable[
                [],
                tuple[list[list[Cell]], list[tuple[int, int]]],
            ]
        ] = None,
    ) -> None:
        self.maze: list[list[Cell]] = maze
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.solution: list[tuple[int, int]] = solution
        self.regenerate_callback: Optional[
            Callable[
                [],
                tuple[list[list[Cell]], list[tuple[int, int]]],
            ]
        ] = regenerate_callback

        self.show_path: bool = False
        self.generation_iterator: Optional[
            Iterator[list[list[Cell]]]
        ] = None
        self.generation_active: bool = False

        self.disco_mode: bool = False
        self.rainbow_mode: bool = False
        self.animation_frame: int = 0

        self.maze_height: int = len(maze)
        self.maze_width: int = len(maze[0])

        self.cell_size: int = self._calculate_cell_size()
        self.maze_width_px: int = self.maze_width * self.cell_size
        self.maze_height_px: int = self.maze_height * self.cell_size

        self.window_width: int = self.maze_width_px
        self.window_height: int = (
            self.maze_height_px + StatusBar.HEIGHT
        )

        self.config: RendererConfig = RendererConfig()
        self.animation: MazeAnimation = MazeAnimation(self.config)

        self.window: MlxWindow = MlxWindow(
            self.window_width,
            self.window_height,
            "A Maze-ing",
        )

        self.mlx = self.window.mlx
        self.mlx_ptr = self.window.mlx_ptr
        self.win_ptr = self.window.win_ptr

        self.image: MlxImage = MlxImage(
            self.mlx,
            self.mlx_ptr,
            self.window_width,
            self.window_height,
            self.win_ptr,
        )

        self.maze_drawer: MazeDrawer = MazeDrawer(
            self.image,
            self.cell_size,
            self.maze_width,
            self.maze_height,
        )

        self.status_bar: StatusBar = StatusBar(
            self.mlx,
            self.mlx_ptr,
            self.win_ptr,
            self.window_width,
            self.maze_height_px,
        )

        self.keyboard: MazeKeyboard = MazeKeyboard(self)

        self.mlx_hooks: MlxHooks = MlxHooks(self)
        self.mlx_hooks.setup()

    def start_generation(
        self,
        generation_iterator: Iterator[list[list[Cell]]],
    ) -> None:
        """Start stepping through a generation iterator inside the MLX loop."""

        self.generation_iterator = generation_iterator
        self.generation_active = True

    def _calculate_cell_size(self) -> int:
        max_width: int = 1200
        max_height: int = 900 - StatusBar.HEIGHT

        width_size: int = max_width // self.maze_width
        height_size: int = max_height // self.maze_height

        return max(10, min(width_size, height_size))

    def render(self) -> None:
        """Render the current maze and status bar."""
        self.image.fill(self.config.background_color)

        if not self.generation_active:
            self._ensure_solution()

        # Draw the image-backed parts first.
        self.maze_drawer.draw_maze(
            self.maze,
            self.solution,
            self.entry,
            self.exit,
            self.show_path,
            self.config.path_color,
            self.config.logo_color,
            self.config.entry_color,
            self.config.exit_color,
            self.config.wall_color,
        )

        self.status_bar.draw(
            self.image,
            self.maze_width,
            self.maze_height,
            self.show_path,
            self.config.wall_color,
            self.config.status_background_color,
            self.config.entry_color,
            self.config.exit_color,
            self.config.path_color,
        )

        # Display the image-backed parts.
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.image.image,
            0,
            0,
        )

        # The maze must also be drawn after the image is displayed.
        self.maze_drawer.draw_maze(
            self.maze,
            self.solution,
            self.entry,
            self.exit,
            self.show_path,
            self.config.path_color,
            self.config.logo_color,
            self.config.entry_color,
            self.config.exit_color,
            self.config.wall_color,
        )

        # Text must be drawn last so it is not covered by the image.
        self.status_bar.draw_text(
            self.maze_width,
            self.maze_height,
            self.show_path,
            self.disco_mode,
            self.rainbow_mode,
            self.maze_height_px,
            self.config.wall_color,
            self.config.background_color,
            self.config.entry_color,
            self.config.exit_color,
            self.config.path_color,
        )

        self.mlx.mlx_do_sync(self.mlx_ptr)

    def _ensure_solution(self) -> None:
        """Calculate the maze solution when it is not already available."""
        if self.solution:
            return

        # Renderer coordinates are (x, y).
        # MazeSolver coordinates are (row, col), or (y, x).
        solver_entry: tuple[int, int] = (self.entry[1], self.entry[0])
        solver_exit: tuple[int, int] = (self.exit[1], self.exit[0])

        self.solution = MazeGenerator.find_path(
            self.maze,
            solver_entry,
            solver_exit,
        )

    def regenerate(self) -> None:
        """Generate a new maze using the configured callback."""
        if self.regenerate_callback is None:
            print("R pressed: no regeneration callback configured")
            return

        try:
            self.maze, self.solution = self.regenerate_callback()

            self.maze_height = len(self.maze)
            self.maze_width = len(self.maze[0])

            self.maze_drawer.maze_width = self.maze_width
            self.maze_drawer.maze_height = self.maze_height

            self.show_path = False
            self.animation_frame = 0

            self.render()

        except Exception as error:
            print(f"Could not regenerate maze: {error}")

    def run(self) -> None:
        """Start the maze renderer."""
        self.render()
        self.mlx.mlx_loop(self.mlx_ptr)

    def close(self) -> None:
        """Release MLX resources and close the window."""
        self.image.destroy()

        if self.win_ptr is not None:
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr,)
            self.win_ptr = None

        if self.mlx_ptr is not None:
            self.mlx.mlx_release(self.mlx_ptr)
            self.mlx_ptr = None
