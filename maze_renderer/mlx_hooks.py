from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from .maze_renderer import MazeRenderer


class MlxHooks:
    """Handle MiniLibX events and animation updates."""

    STEPS_PER_FRAME = 5

    def __init__(self, renderer: "MazeRenderer") -> None:
        self.renderer = renderer

    def setup(self) -> None:
        """Register MiniLibX event hooks."""
        renderer = self.renderer

        renderer.mlx.mlx_key_hook(
            renderer.win_ptr,
            self.on_key,
            None,
        )

        renderer.mlx.mlx_expose_hook(
            renderer.win_ptr,
            self.on_expose,
            None,
        )

        renderer.mlx.mlx_hook(
            renderer.win_ptr,
            33,
            0,
            self.on_close,
            None,
        )

        renderer.mlx.mlx_loop_hook(
            renderer.mlx_ptr,
            self.animation_loop,
            None,
        )

    def on_key(self, key: int, param: Any) -> int:
        """Handle keyboard input."""
        return self.renderer.keyboard.handle(key, param)

    def on_close(self, _param: Any) -> int:
        """Close the application."""
        self.renderer.close()
        return 0

    def on_expose(self, _param: Any) -> int:
        """Redraw the window when exposed."""
        self.renderer.render()
        return 0

    def animation_loop(self, _param: Any) -> int:
        """Advance maze generation or colour animation."""
        renderer = self.renderer

        if renderer.generation_active:
            self._advance_generation()
            return 0

        if not renderer.disco_mode and not renderer.rainbow_mode:
            return 0

        renderer.animation_frame += 1

        # Around 20 colour animation updates per second.
        if renderer.animation_frame % 5 != 0:
            return 0

        if renderer.disco_mode:
            renderer.animation.disco_colors()
        elif renderer.rainbow_mode:
            renderer.animation.rainbow_colors(
                renderer.animation_frame
            )

        renderer.render()

        return 0

    def _advance_generation(self) -> None:
        """Advance several maze generation steps per frame."""
        renderer = self.renderer

        if renderer.generation_iterator is None:
            renderer.generation_active = False
            return

        try:
            for _ in range(self.STEPS_PER_FRAME):
                next(renderer.generation_iterator)
        except StopIteration:
            renderer.generation_iterator = None
            renderer.generation_active = False

        renderer.render()
