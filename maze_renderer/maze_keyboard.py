from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from .maze_renderer import MazeRenderer


class MazeKeyboard:
    """Handle keyboard input for the maze renderer."""

    def __init__(self, renderer: "MazeRenderer") -> None:
        """Initialize the keyboard handler.

        Args:
            renderer: Maze renderer controlled by the keyboard.
        """
        self.renderer: "MazeRenderer" = renderer

    def handle(self, key: int, _param: Any) -> int:
        """Handle a keyboard event.

        Args:
            key: Key code received from MiniLibX.
            _param: Callback parameter provided by MiniLibX.

        Returns:
            Zero to indicate successful event handling.
        """
        if key == self.renderer.KEY_ESC:
            self.renderer.close()

        elif key == self.renderer.KEY_P:
            self.renderer.show_path = not self.renderer.show_path
            self.renderer.render()

        elif key == self.renderer.KEY_R:
            self.renderer.regenerate()

        elif key == self.renderer.KEY_C:
            self.renderer.config.next_wall_color()
            self.renderer.render()

        elif key == self.renderer.KEY_B:
            self.renderer.config.next_background_color()
            self.renderer.render()

        elif key == self.renderer.KEY_E:
            self.renderer.config.next_entry_color()
            self.renderer.render()

        elif key == self.renderer.KEY_X:
            self.renderer.config.next_exit_color()
            self.renderer.render()

        elif key == self.renderer.KEY_S:
            self.renderer.config.next_path_color()
            self.renderer.render()

        elif key == self.renderer.KEY_L:
            self.renderer.config.next_logo_color()
            self.renderer.render()

        elif key == self.renderer.KEY_D:
            self.renderer.disco_mode = not self.renderer.disco_mode

            # Only one animation mode can be active.
            if self.renderer.disco_mode:
                self.renderer.rainbow_mode = False

            self.renderer.render()

        elif key == self.renderer.KEY_V:
            self.renderer.rainbow_mode = not self.renderer.rainbow_mode

            # Only one animation mode can be active.
            if self.renderer.rainbow_mode:
                self.renderer.disco_mode = False

            self.renderer.render()

        return 0
