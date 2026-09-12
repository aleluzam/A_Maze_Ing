import colorsys
import random

from .renderer_config import RendererConfig


class MazeAnimation:
    """Utility for animated colour changes in the maze renderer.

    Provides two animation modes:
    * ``disco_colors`` – picks completely random colours for each UI element.
    * ``rainbow_colors`` – smoothly cycles colours based on the current frame,
      giving a rainbow effect.
    """
    def __init__(self, config: RendererConfig) -> None:
        """Store a reference to the renderer configuration.

        Args:
            config: The :class:`RendererConfig` instance whose colour fields
            will be mutated by the animation methods.
        """
        self.config = config

    def disco_colors(self) -> None:
        """Generate a new random colour palette."""
        self.config.wall_color = self._random_color()

        # Keep the background relatively dark so the maze remains visible.
        self.config.background_color = self._random_color()
        self.config.entry_color = self._random_color()
        self.config.exit_color = self._random_color()
        self.config.path_color = self._random_color()
        self.config.logo_color = self._random_color()

    def rainbow_colors(self, frame: int) -> None:
        """Generate a smoothly changing rainbow palette.

        Different elements use different offsets so that they
        don't all have exactly the same colour.
        """
        hue = (frame % 360) / 360.0

        self.config.wall_color = self._hsv_to_rgb(hue)

        self.config.background_color = self._hsv_to_rgb(
            hue + 0.50,
            saturation=0.75,
            value=0.15,
        )

        self.config.entry_color = self._hsv_to_rgb(hue + 0.16)
        self.config.exit_color = self._hsv_to_rgb(hue + 0.66)
        self.config.path_color = self._hsv_to_rgb(hue + 0.33)

    @staticmethod
    def _random_color() -> int:
        """Generate a random colour"""
        return random.randint(0x000000, 0xFFFFFF)

    @staticmethod
    def _hsv_to_rgb(
        hue: float,
        saturation: float = 1.0,
        value: float = 1.0,
    ) -> int:
        """Convert HSV values to a MiniLibX‑compatible RGB integer.
        hue is allowed to go above 1.0 because it wraps around."""
        hue %= 1.0

        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)

        return (
            (int(red * 255) << 16) | (int(green * 255) << 8) | int(blue * 255)
        )
