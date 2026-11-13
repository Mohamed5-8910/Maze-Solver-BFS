"""Breadth-first search for four-directional, unit-cost mazes."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Sequence, TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = Sequence[Sequence[int]]


@dataclass(frozen=True)
class SearchResult:
    """Outcome of a BFS run.

    explored_nodes lists cells removed from the FIFO queue and processed, in
    order. It includes the goal when found. explored_count is its length.
    """

    found: bool
    path: list[Coordinate]
    explored_nodes: list[Coordinate]
    path_cost: int | None

    @property
    def explored_count(self) -> int:
        """Number of processed nodes (including the goal if reached)."""
        return len(self.explored_nodes)


def _validate_grid(grid: Grid) -> tuple[int, int]:
    if not grid:
        raise ValueError("Grid must contain at least one row.")
    if not grid[0]:
        raise ValueError("Grid rows must contain at least one cell.")
    columns = len(grid[0])
    for row_index, row in enumerate(grid):
        if len(row) != columns:
            raise ValueError("Grid must be rectangular; row lengths differ.")
        for column_index, value in enumerate(row):
            if type(value) is not int or value not in (0, 1):
                raise ValueError(
                    f"Unsupported cell value at ({row_index}, {column_index}); use 0 or 1."
                )
    return len(grid), columns


def _validate_coordinate(position: Coordinate, name: str, rows: int, columns: int) -> None:
    if (not isinstance(position, tuple) or len(position) != 2
            or any(type(part) is not int for part in position)):
        raise ValueError(f"{name} must be a (row, column) integer tuple.")
    row, column = position
    if not (0 <= row < rows and 0 <= column < columns):
        raise ValueError(f"{name} {position} is outside the grid.")


def solve_maze(grid: Grid, start: Coordinate, goal: Coordinate) -> SearchResult:
    """Find a minimum-move path with BFS, or return an unsuccessful result.

    0 represents a traversable cell and 1 an obstacle. Invalid grids or
    coordinates raise ValueError. Neighbor order is up, down, left, right.
    """
    rows, columns = _validate_grid(grid)
    _validate_coordinate(start, "Start", rows, columns)
    _validate_coordinate(goal, "Goal", rows, columns)
    if grid[start[0]][start[1]] == 1:
        raise ValueError("Start cell is blocked.")
    if grid[goal[0]][goal[1]] == 1:
        raise ValueError("Goal cell is blocked.")

    queue = deque([start])
    discovered = {start}
    predecessor: dict[Coordinate, Coordinate | None] = {start: None}
    explored: list[Coordinate] = []
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    while queue:
        current = queue.popleft()
        explored.append(current)
        if current == goal:
            path: list[Coordinate] = []
            cursor: Coordinate | None = goal
            while cursor is not None:
                path.append(cursor)
                cursor = predecessor[cursor]
            path.reverse()
            return SearchResult(True, path, explored, len(path) - 1)

        for row_delta, column_delta in directions:
            neighbor = (current[0] + row_delta, current[1] + column_delta)
            row, column = neighbor
            if (0 <= row < rows and 0 <= column < columns
                    and grid[row][column] == 0 and neighbor not in discovered):
                discovered.add(neighbor)
                predecessor[neighbor] = current
                queue.append(neighbor)

    return SearchResult(False, [], explored, None)
