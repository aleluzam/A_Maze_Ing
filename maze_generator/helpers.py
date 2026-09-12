import random
from collections import deque
from collections.abc import Iterator
from typing import Optional
from .models import Cell, CellStatus, Direction
from .models import MazeError


def open_all_walls(maze: list[list[Cell]], position: tuple[int, int]) -> None:
    """Open all walls of a cell except those facing outside the maze bounds"""
    try:
        row, col = position
        rows = len(maze)
        cols = len(maze[0])
        cell = maze[row][col]

        cell.north = row == 0
        cell.south = row == rows - 1
        cell.west = col == 0
        cell.east = col == cols - 1

        if row > 0:
            maze[row - 1][col].south = cell.north
        if row < rows - 1:
            maze[row + 1][col].north = cell.south
        if col > 0:
            maze[row][col - 1].east = cell.west
        if col < cols - 1:
            maze[row][col + 1].west = cell.east
    except (IndexError, TypeError) as e:
        raise MazeError("invalid cell position") from e


def get_neighbors(
    maze: list[list[Cell]],
    position: tuple[int, int],
) -> list[tuple[int, int]]:
    """Get all neighbors: allow and adjacent Cells"""
    try:
        neighbor: list[tuple[int, int]] = []

        row, col = position
        rows = len(maze)
        cols = len(maze[0])

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # delta row, delta column
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            in_row_bounds = 0 <= new_row < rows
            in_col_bounds = 0 <= new_col < cols

            if in_row_bounds and in_col_bounds:
                is_default = (
                    maze[new_row][new_col].status == CellStatus.DEFAULT
                )

                if is_default:
                    neighbor.append((new_row, new_col))

        return neighbor
    except (IndexError, TypeError) as e:
        raise MazeError("cannot get neighbors for invalid position") from e


def select_neighbor(
    neighbor: list[tuple[int, int]],
    rng: random.Random,
) -> tuple[int, int]:
    """Randomly select a neighbor"""
    try:
        return rng.choice(neighbor)
    except IndexError as e:
        raise MazeError("no neighbor to select") from e


def create_closed_maze(width: int, height: int) -> list[list[Cell]]:
    """Create a maze grid with all walls closed."""
    try:
        return [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]
    except MemoryError as e:
        raise MazeError("failed to allocate maze grid") from e
    except ValueError as e:
        raise MazeError("invalid maze dimensions") from e


def break_wall(
    maze: list[list[Cell]],
    actual_pos: tuple[int, int],
    nex_pos: tuple[int, int],
) -> None:
    """Break walls pair"""
    try:
        if actual_pos[0] != nex_pos[0]:
            if actual_pos[0] < nex_pos[0]:
                # down
                maze[actual_pos[0]][actual_pos[1]].open_wall(Direction.SOUTH)
                maze[nex_pos[0]][nex_pos[1]].open_wall(Direction.NORTH)
            else:
                # up
                maze[actual_pos[0]][actual_pos[1]].open_wall(Direction.NORTH)
                maze[nex_pos[0]][nex_pos[1]].open_wall(Direction.SOUTH)
        else:
            if actual_pos[1] < nex_pos[1]:
                # right
                maze[actual_pos[0]][actual_pos[1]].open_wall(Direction.EAST)
                maze[nex_pos[0]][nex_pos[1]].open_wall(Direction.WEST)
            else:
                # left
                maze[actual_pos[0]][actual_pos[1]].open_wall(Direction.WEST)
                maze[nex_pos[0]][nex_pos[1]].open_wall(Direction.EAST)
    except (IndexError, TypeError) as e:
        raise MazeError("invalid wall break positions") from e


def generate_42logo(maze: list[list[Cell]]) -> None:
    """Generate the 42 logo in maze center"""
    min_width = 9
    min_height = 9
    if len(maze[0]) < min_width or len(maze) < min_height:
        print("Maze too small for 42 logo – pattern omitted.")
        return
    try:
        coordinates: tuple[tuple[int, int], ...] = (
            (-3, -2), (-3, -1), (-3, 0), (-2, 0),
            (-1, 0), (-1, 1),
            (-1, 2), (1, -2), (2, -2), (3, -2),
            (3, -1), (3, 0), (2, 0), (1, 0),
            (1, 1), (1, 2), (2, 2), (3, 2)
        )
        cx = len(maze[0]) // 2
        cy = len(maze) // 2

        for x, y in coordinates:
            maze[cy + y][cx + x].status = CellStatus.LOGO
    except Exception as e:
        raise MazeError("failed to place 42 logo") from e


# (delta_row, delta_col, current_wall, opposite_wall_in_neighbour)
DIRECTIONS = (
    (-1, 0, "north", "south"),
    (0, 1, "east", "west"),
    (1, 0, "south", "north"),
    (0, -1, "west", "east"),
)


def inside(cell: tuple[int, int], rows: int, cols: int) -> bool:
    row, col = cell
    return 0 <= row < rows and 0 <= col < cols


def can_move(
    current_cell: Cell,
    neighbour_cell: Cell,
    wall: str,
    opposite_wall: str,
) -> bool:
    current_open = not getattr(current_cell, wall)
    neighbour_open = not getattr(neighbour_cell, opposite_wall)

    return current_open and neighbour_open


def reachable_neighbours(
    maze: list[list[Cell]],
    position: tuple[int, int],
    rows: int,
    cols: int,
    visited: dict[tuple[int, int], Optional[tuple[int, int]]],
) -> Iterator[tuple[int, int]]:
    row, col = position
    current_cell = maze[row][col]

    for d_row, d_col, wall, opposite_wall in DIRECTIONS:
        next_pos = (row + d_row, col + d_col)

        if not inside(next_pos, rows, cols):
            continue
        if next_pos in visited:
            continue

        neighbour_cell = maze[next_pos[0]][next_pos[1]]

        if not can_move(current_cell, neighbour_cell, wall, opposite_wall):
            continue

        yield next_pos


def bfs(
    maze: list[list[Cell]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    rows: int,
    cols: int,
) -> dict[tuple[int, int], Optional[tuple[int, int]]]:
    queue = deque([entry])
    parents: dict[tuple[int, int], Optional[tuple[int, int]]] = {entry: None}

    while queue:
        position = queue.popleft()

        if position == exit:
            break

        for next_pos in reachable_neighbours(
                maze,
                position,
                rows,
                cols,
                parents
        ):
            parents[next_pos] = position
            queue.append(next_pos)

    return parents


def reconstruct_path(
    parents: dict[tuple[int, int], Optional[tuple[int, int]]],
    exit: tuple[int, int],
) -> list[tuple[int, int]]:
    if exit not in parents:
        return []

    path: list[tuple[int, int]] = []
    current: Optional[tuple[int, int]] = exit

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def open_maze_borders(maze: list[list[Cell]]) -> list[list[Cell]]:
    try:
        rows = len(maze)
        cols = len(maze[0])
        for r, row in enumerate(maze):
            for c, cell in enumerate(row):
                if cell.status == CellStatus.BORDER:

                    # 1. Top-left corner (r == 0, c == 0)
                    if r == 0 and c == 0:
                        cell.north = True
                        cell.west = True
                        cell.east = False
                        cell.south = False

                    # 2. Top-right corner (r == 0, c == cols - 1)
                    elif r == 0 and c == cols - 1:
                        cell.north = True
                        cell.east = True
                        cell.west = False

                    # 3. Bottom-left corner (r == rows - 1, c == 0)
                    elif r == rows - 1 and c == 0:
                        cell.south = True
                        cell.west = True
                        cell.east = False

                    # 4. Bottom-right corner
                    elif r == rows - 1 and c == cols - 1:
                        cell.south = True
                        cell.east = True
                        cell.west = False

                    # 5. Entire top row (excluding corners)
                    elif r == 0:
                        cell.north = True
                        cell.west = False
                        cell.east = False

                    # 6. Entire bottom row (excluding corners)
                    elif r == rows - 1:
                        cell.south = True
                        cell.west = False
                        cell.east = False

                    # 7. Entire left column (excluding corners)
                    elif c == 0:
                        cell.west = True
                        cell.north = False
                        cell.south = False

                    # 8. Entire right column (excluding corners)
                    elif c == cols - 1:
                        cell.east = True
                        cell.north = False
                        cell.south = False

        return maze
    except Exception as e:
        raise MazeError("failed to process maze borders") from e
