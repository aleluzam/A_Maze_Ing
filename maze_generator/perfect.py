from typing import Iterator
import random
import secrets

from .models import Cell, CellStatus
from .helpers import (
    generate_42logo,
    get_neighbors,
    select_neighbor,
    break_wall
)

from .models import MazeError


def generate_perfect_maze_steps(
    maze: list[list[Cell]],
    start: tuple[int, int],
    end: tuple[int, int],
    seed: str | None,
) -> Iterator[list[list[Cell]]]:
    """Yield the maze after every generation step."""
    try:
        # validations
        generate_42logo(maze)

        if seed is None:
            seed = secrets.token_hex(8)

        rng = random.Random(seed)
        rng.random()

        stack: list[tuple[int, int]] = []
        stack.append(start)
        maze[start[0]][start[1]].status = CellStatus.START
        yield maze

        while stack:
            actual_pos: tuple[int, int] = stack[-1]
            neighbor: list[tuple[int, int]] = get_neighbors(maze, actual_pos)
            if neighbor:
                nex_pos: tuple[int, int] = select_neighbor(neighbor, rng)
                break_wall(maze, actual_pos, nex_pos)
                maze[nex_pos[0]][nex_pos[1]].status = CellStatus.MID
                stack.append(nex_pos)
            else:
                stack.pop()
            yield maze
    except Exception as e:
        raise MazeError("perfect maze step generation failed") from e


def generate_perfect_maze(
    maze: list[list[Cell]],
    start: tuple[int, int],
    end: tuple[int, int],
    seed: str | None,
) -> list[list[Cell]]:
    """Generate a perfect maze."""
    try:
        for _ in generate_perfect_maze_steps(maze, start, end, seed):
            pass
        return maze
    except Exception as e:
        raise MazeError("perfect maze generation failed") from e
