"""Models used by the maze generator."""

from enum import Enum

from pydantic import BaseModel


class Direction(str, Enum):
    """Cardinal directions."""

    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"


class CellStatus(str, Enum):
    """Visual status of a maze cell."""

    DEFAULT = "default"
    START = "start"
    MID = "mid"
    LOGO = "logo42"
    BORDER = "border"


class Cell(BaseModel):
    """Represent one maze cell."""

    # True means the wall is closed.
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
    status: CellStatus = CellStatus.DEFAULT

    def open_wall(self, direction: Direction) -> None:
        """Open a wall in the specified direction.

        Args:
            direction: Wall to open.
        """
        setattr(self, direction.value, False)

    def to_hex(self) -> str:
        """Return the closed walls as one hexadecimal digit."""
        value = sum(
            int(wall) * weight
            for wall, weight in zip(
                (self.north, self.east, self.south, self.west),
                (1, 2, 4, 8),
            )
        )
        return format(value, "x")


class MazeError(Exception):
    """Represent an error raised by the maze generator."""

    def __init__(
        self,
        message: str = "Internal MazeGenerator error",
    ) -> None:
        """Initialize a maze error.

        Args:
            message: Description of the error.
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """Return the error message.

        Returns:
            The error message.
        """
        return self.message
