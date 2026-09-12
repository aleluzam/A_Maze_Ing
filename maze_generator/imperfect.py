import secrets
import random
from .models import Cell, CellStatus, MazeError
from .helpers import open_maze_borders


def closed_doors(cell: Cell) -> list[str]:
    """Return a list of closed directions for a cell."""
    directions: list[str] = []
    if cell.north:
        directions.append("north")
    if cell.east:
        directions.append("east")
    if cell.south:
        directions.append("south")
    if cell.west:
        directions.append("west")
    return directions


def set_border_status(grid: list[list[Cell]]) -> list[list[Cell]]:
    """Set border cells status to: BORDER"""
    try:
        rows = len(grid)
        cols = len(grid[0])
        for row in range(rows):
            for col in range(cols):
                if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                    grid[row][col].status = CellStatus.BORDER
        return grid
    except Exception as e:
        raise MazeError("failed to set border status") from e


def are_dead_ends(maze: list[list[Cell]]) -> bool:
    """Check if the maze still contains dead‑end cells.

    A dead end is a cell with exactly three closed doors (walls) while its
    status is ``DEFAULT``, ``MID`` or ``START``.
    """
    try:
        for row in maze:
            for cell in row:
                is_open = cell.status in (
                    CellStatus.DEFAULT, CellStatus.MID,
                    CellStatus.START
                )
                has_three_closed_doors = len(closed_doors(cell)) == 3
                if is_open and has_three_closed_doors:
                    return True
        return False
    except Exception as e:
        raise MazeError("dead‑end check failed") from e


def open_door(
    maze: list[list[Cell]],
    position: tuple[int, int],
    rng: random.Random,
) -> None:
    """Open a random closed door of *position* if possible.

    The function selects a random direction from the list of doors that can be
    opened (i.e., the neighbour exists, is within bounds, and has a suitable
    status) and removes the wall between the current cell and that neighbour.
    """
    try:
        doors_to_open = get_openable_doors(maze, position)
        row, col = position
        if doors_to_open:
            direction = rng.choice(doors_to_open)
            setattr(maze[row][col], direction, False)
            if direction == "north":
                maze[row - 1][col].south = False
            elif direction == "south":
                maze[row + 1][col].north = False
            elif direction == "east":
                maze[row][col + 1].west = False
            elif direction == "west":
                maze[row][col - 1].east = False
    except Exception as e:
        raise MazeError("failed to open door") from e


def get_openable_doors(
        maze: list[list[Cell]],
        position: tuple[int, int]
) -> list[str]:
    """Return a list of directions whose walls can be opened.

    A door is openable when the neighbour cell lies within the maze bounds and
    its status is ``DEFAULT``, ``MID`` or ``START``.
    """
    try:
        row, col = position
        rows = len(maze)
        cols = len(maze[0])
        directions = {
            "north": (-1, 0),
            "east": (0, 1),
            "south": (1, 0),
            "west": (0, -1),
        }
        openable_doors: list[str] = []
        for direction, (dr, dc) in directions.items():
            new_row = row + dr
            new_col = col + dc
            has_direction = getattr(maze[row][col], direction)
            in_row_bounds = 0 <= new_row < rows
            in_col_bounds = 0 <= new_col < cols
            if has_direction and in_row_bounds and in_col_bounds:
                neighbor_status = maze[new_row][new_col].status
                if neighbor_status in (
                    CellStatus.DEFAULT,
                    CellStatus.MID,
                    CellStatus.START,
                ):
                    openable_doors.append(direction)
        return openable_doors
    except Exception as e:
        raise MazeError("failed to list openable doors") from e


def imperfect_generation(
    maze: list[list[Cell]],
    seed: str | None,
) -> list[list[Cell]]:
    """Transform a perfect maze into an imperfect one removing dead‑end walls.

    The algorithm repeatedly finds cells that have exactly three closed doors
    (i.e., dead ends) and opens a random adjacent wall. This process continues
    until no dead ends remain or no further walls can be opened, ensuring the
    resulting maze contains loops while keeping the 42 logo intact.

    Args:
        maze: A perfect maze represented as a grid of :class:`Cell` objects.
        seed: Optional random seed; if ``None`` a fresh seed is generated.

    Returns:
        The modified maze with loops introduced.
    """
    try:
        if seed is None:
            seed = secrets.token_hex(8)
        rng = random.Random(seed)
        while True:
            dead_ends: list[tuple[int, int]] = []
            for row, cells in enumerate(maze):
                for col, cell in enumerate(cells):
                    has_three_closed_doors = len(closed_doors(cell)) == 3
                    has_valid_status = cell.status in (
                        CellStatus.DEFAULT, CellStatus.MID,
                        CellStatus.START
                    )
                    if has_three_closed_doors and has_valid_status:
                        dead_ends.append((row, col))
            if not dead_ends:
                break
            doors_opened = False
            for row, col in dead_ends:
                doors_before = len(closed_doors(maze[row][col]))
                open_door(maze, (row, col), rng)
                doors_after = len(closed_doors(maze[row][col]))
                if doors_after < doors_before:
                    doors_opened = True
            if not doors_opened:
                break
        return maze
    except Exception as e:
        raise MazeError("imperfect maze generation failed") from e


def generate_no_perfect_maze(
    maze: list[list[Cell]],
    seed: str | None,
) -> list[list[Cell]]:
    """Turn a perfect maze into an imperfect maze.

    The function first calls :func:`imperfect_generation` to break dead ends,
    then marks border cells and opens the maze borders.
    """
    try:
        maze = imperfect_generation(maze, seed)
        maze = set_border_status(maze)
        maze = open_maze_borders(maze)
        return maze
    except Exception as e:
        raise MazeError("failed to generate no‑perfect maze") from e
