from dataclasses import dataclass


@dataclass
class RendererConfig:
    """Configuration holder for colours used by the maze renderer.

    The fields store integer RGB values (0xRRGGBB). Helper methods cycle each
    colour through a predefined palette, allowing the user to change the
    appearance interactively via keyboard shortcuts.
    """
    background_color: int = 0x101820
    status_background_color: int = 0x202020
    wall_color: int = 0xFFFFFF
    entry_color: int = 0x00FF00
    exit_color: int = 0xFF0000
    path_color: int = 0x00FFFF
    logo_color: int = 0xFFD700

    background_colours: tuple[int, ...] = (
        0x101820,
        0x000000,
        0x202020,
        0x102030,
        0x201020,
        0x202010,
    )

    wall_colours: tuple[int, ...] = (
        0xFFFFFF,
        0xFFFF00,
        0x00FFFF,
        0x00FF00,
        0xFF00FF,
    )

    entry_colours: tuple[int, ...] = (
        0x00FF00,
        0x00FFFF,
        0xFFFFFF,
        0xFFFF00,
    )

    exit_colours: tuple[int, ...] = (
        0xFF0000,
        0xFF00FF,
        0xFFFF00,
        0xFFFFFF,
    )

    path_colours: tuple[int, ...] = (
        0x00FFFF,
        0x00FF00,
        0xFFFF00,
        0xFF00FF,
        0xFFFFFF,
    )

    logo_colours: tuple[int, ...] = (
        0xFFD700,
        0xFF00FF,
        0x00FFFF,
        0x00FF00,
        0xFFFFFF,
    )

    background_colour_index: int = 0
    wall_colour_index: int = 0
    entry_colour_index: int = 0
    exit_colour_index: int = 0
    path_colour_index: int = 0
    logo_colour_index: int = 0

    def next_background_color(self) -> None:
        """Switch to the next background colour."""
        self.background_colour_index, self.background_color = self._next(
            self.background_colour_index,
            self.background_colours,
        )

    def next_wall_color(self) -> None:
        """Switch to the next wall colour."""
        self.wall_colour_index, self.wall_color = self._next(
            self.wall_colour_index,
            self.wall_colours,
        )

    def next_entry_color(self) -> None:
        """Switch to the next entry colour."""
        self.entry_colour_index, self.entry_color = self._next(
            self.entry_colour_index,
            self.entry_colours,
        )

    def next_exit_color(self) -> None:
        """Switch to the next exit colour."""
        self.exit_colour_index, self.exit_color = self._next(
            self.exit_colour_index,
            self.exit_colours,
        )

    def next_path_color(self) -> None:
        """Switch to the next path colour."""
        self.path_colour_index, self.path_color = self._next(
            self.path_colour_index,
            self.path_colours,
        )

    def next_logo_color(self) -> None:
        """Switch to the next logo colour."""
        self.logo_colour_index, self.logo_color = self._next(
            self.logo_colour_index,
            self.logo_colours,
        )

    @staticmethod
    def _next(index: int, colours: tuple[int, ...],) -> tuple[int, int]:
        """Return the next colour index and colour.

        Args:
            index: Current colour index.
            colours: Available colours.

        Returns:
            A tuple containing the next index and colour.
        """
        index = (index + 1) % len(colours)
        return index, colours[index]
