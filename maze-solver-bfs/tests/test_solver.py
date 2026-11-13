"""Unit tests for the pure maze BFS implementation."""

import unittest

from maze_solver.solver import solve_maze


class SolverTests(unittest.TestCase):
    def assert_valid_path(self, grid, start, goal, result):
        self.assertTrue(result.found)
        self.assertEqual(result.path[0], start)
        self.assertEqual(result.path[-1], goal)
        for row, column in result.path:
            self.assertTrue(0 <= row < len(grid) and 0 <= column < len(grid[0]))
            self.assertEqual(grid[row][column], 0)
        for first, second in zip(result.path, result.path[1:]):
            self.assertEqual(abs(first[0] - second[0]) + abs(first[1] - second[1]), 1)
        self.assertEqual(result.path_cost, len(result.path) - 1)

    def test_simple_route(self):
        grid = [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
        result = solve_maze(grid, (0, 0), (2, 2))
        self.assert_valid_path(grid, (0, 0), (2, 2), result)
        self.assertEqual(result.path_cost, 4)

    def test_detour_around_obstacles(self):
        grid = [[0, 1, 0], [0, 1, 0], [0, 0, 0]]
        result = solve_maze(grid, (0, 0), (0, 2))
        self.assert_valid_path(grid, (0, 0), (0, 2), result)
        self.assertEqual(result.path_cost, 6)

    def test_unreachable_goal_and_exploration_count(self):
        grid = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
        result = solve_maze(grid, (0, 0), (0, 2))
        self.assertFalse(result.found)
        self.assertEqual(result.path, [])
        self.assertIsNone(result.path_cost)
        self.assertEqual(result.explored_nodes, [(0, 0), (1, 0), (2, 0)])
        self.assertEqual(result.explored_count, len(result.explored_nodes))

    def test_start_equals_goal(self):
        result = solve_maze([[0]], (0, 0), (0, 0))
        self.assertTrue(result.found)
        self.assertEqual(result.path, [(0, 0)])
        self.assertEqual(result.path_cost, 0)
        self.assertEqual(result.explored_nodes, [(0, 0)])
        self.assertEqual(result.explored_count, 1)

    def test_blocked_start(self):
        with self.assertRaisesRegex(ValueError, "Start cell is blocked"):
            solve_maze([[1, 0]], (0, 0), (0, 1))

    def test_blocked_goal(self):
        with self.assertRaisesRegex(ValueError, "Goal cell is blocked"):
            solve_maze([[0, 1]], (0, 0), (0, 1))

    def test_out_of_bounds_coordinate(self):
        with self.assertRaisesRegex(ValueError, "outside the grid"):
            solve_maze([[0]], (0, 0), (1, 0))

    def test_empty_grid(self):
        with self.assertRaisesRegex(ValueError, "at least one row"):
            solve_maze([], (0, 0), (0, 0))

    def test_empty_row(self):
        with self.assertRaisesRegex(ValueError, "at least one cell"):
            solve_maze([[]], (0, 0), (0, 0))

    def test_non_rectangular_grid(self):
        with self.assertRaisesRegex(ValueError, "rectangular"):
            solve_maze([[0, 0], [0]], (0, 0), (0, 0))

    def test_invalid_cell_value(self):
        with self.assertRaisesRegex(ValueError, "Unsupported cell value"):
            solve_maze([[0, 2]], (0, 0), (0, 1))

    def test_single_traversable_cell(self):
        result = solve_maze([[0]], (0, 0), (0, 0))
        self.assert_valid_path([[0]], (0, 0), (0, 0), result)

    def test_boundary_route_stays_inside_grid(self):
        grid = [[0, 0], [0, 1]]
        result = solve_maze(grid, (0, 0), (1, 0))
        self.assert_valid_path(grid, (0, 0), (1, 0), result)

    def test_path_has_minimum_moves(self):
        grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        result = solve_maze(grid, (0, 0), (2, 2))
        self.assert_valid_path(grid, (0, 0), (2, 2), result)
        self.assertEqual(result.path_cost, 4)

    def test_results_are_deterministic(self):
        grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        first = solve_maze(grid, (1, 1), (0, 0))
        second = solve_maze(grid, (1, 1), (0, 0))
        self.assertEqual(first, second)
        self.assertEqual(first.path, [(1, 1), (0, 1), (0, 0)])


if __name__ == "__main__":
    unittest.main()
