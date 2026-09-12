from typing import Any


class StatusBar:
    """Display controls and status information below the maze."""

    HEIGHT: int = 160

    def __init__(
        self,
        mlx: Any,
        mlx_ptr: Any,
        win_ptr: Any,
        window_width: int,
        maze_height_px: int,
    ) -> None:
        """Initialize the status bar.

        Args:
            mlx: MiniLibX instance.
            mlx_ptr: MiniLibX connection pointer.
            win_ptr: MiniLibX window pointer.
            window_width: Width of the application window in pixels.
            maze_height_px: Maze height in pixels.
        """
        self.mlx: Any = mlx
        self.mlx_ptr: Any = mlx_ptr
        self.win_ptr: Any = win_ptr
        self.window_width: int = window_width
        self.maze_height_px: int = maze_height_px

    def draw(
        self,
        image: Any,
        maze_width: int,
        maze_height: int,
        show_path: bool,
        wall_color: int,
        background_color: int,
        entry_color: int,
        exit_color: int,
        path_color: int,
    ) -> None:
        """Draw the status bar background."""
        start_y: int = self.maze_height_px

        for y in range(start_y, start_y + self.HEIGHT):
            for x in range(self.window_width):
                image.put_pixel(x, y, background_color)

    def draw_text(
        self,
        maze_width: int,
        maze_height: int,
        show_path: bool,
        disco_mode: bool,
        rainbow_mode: bool,
        maze_height_px: int,
        wall_color: int,
        background_color: int,
        entry_color: int,
        exit_color: int,
        path_color: int,
    ) -> None:
        """Draw basic controls and current state."""

        y: int = maze_height_px + 20

        commands1: str = (
            "R: Regenerate   "
            "P: Path         "
            "C: Walls        "
            "B: Background   "
            ""
            "ESC: quit       "
        )
        commands2: str = (
            "E: Entry   "
            "X: Ending  "
            "S: Solution   "
            "L: Logo   "
            "D: Disco   "
            "V: Rainbow   "
            "ESC: Quit"
        )

        if disco_mode:
            mode: str = "Mode: DISCO"
        elif rainbow_mode:
            mode = "Mode: RAINBOW"
        else:
            mode = "Mode: Normal"

        self._text(
            commands1,
            10,
            y,
            wall_color,
        )

        path: str = "Path: ON" if show_path else "Path: OFF"

        state: str = f"{mode}    {path}    Maze: {maze_width} x {maze_height}"

        self._text(
            state,
            10,
            y + 20,
            wall_color,
        )

        self._text(
            commands1[:-16],
            10,
            y + 40,
            wall_color,
        )

        self._text(
            commands2[:-12],
            10,
            y + 60,
            wall_color,
        )

        self._text(
            f"Entry: #{entry_color & 0xFFFFFF:06X}",
            10,
            y + 100,
            self._visible_color(entry_color),
        )

        self._text(
            f"Wall: #{wall_color & 0xFFFFFF:06X}",
            200,
            y + 100,
            self._visible_color(wall_color),
        )

        self._text(
            f"Exit: #{exit_color & 0xFFFFFF:06X}",
            370,
            y + 100,
            self._visible_color(exit_color),
        )

        self._text(
            f"Path: #{path_color & 0xFFFFFF:06X}",
            550,
            y + 100,
            self._visible_color(path_color),
        )

    def _visible_color(self, color: int) -> int:
        """Return a visible color, replacing black with white.

        Args:
            color: RGB color encoded as an integer.

        Returns:
            A visible RGB color.
        """
        color &= 0xFFFFFF

        if color == 0:
            return 0xFFFFFF

        return color

    def _text(self, text: str, x: int, y: int, color: int,) -> None:
        """Draw text to the MLX window.

        Args:
            text: Text to display.
            x: Horizontal position in pixels.
            y: Vertical position in pixels.
            color: Text color.
        """
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr, x, y, color, text)
