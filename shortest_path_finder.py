#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
I'm trying to use TDD here
"""

from pathlib import Path
from typing import Dict, List, Tuple
from unittest.result import TestResult

import numpy as np

Point = Tuple


def convert_file_to_array_map(filename: str) -> np.ndarray:
    file = Path(filename)
    assert file.exists()

    lines = []
    with open(file) as f:
        for line in f.readlines():
            binary_line = []
            for point in line:
                if point == '.':
                    binary_line.append(0)
                elif point == '#':
                    binary_line.append(1)
                elif point == '\n':
                    continue
                else:
                    raise ValueError(f"Unknown character in map file: {point}")
            lines.append(binary_line)

    return np.array(lines, dtype=int)

def convert_path_to_string(shortest_path: List[Point]) -> str:
    if not shortest_path:
        return ''

    assert len(shortest_path) >= 2, f'Minimum path should be of length 2 ({len(shortest_path)} was provided)!'
    res = []
    for i in range(0, len(shortest_path)-1):
        current, next = shortest_path[i], shortest_path[i+1]
        row_diff = next[0] - current[0]
        col_diff = next[1] - current[1]

        if row_diff == +1:
            res.append('D')
        elif row_diff == -1:
            res.append('U')
        elif col_diff == +1:
            res.append('R')
        elif col_diff == -1:
            res.append('L')
        else:
            raise AssertionError(f'Wrong move: from {current} to the {next}')
    return ''.join(res)

class ShortestPathFinder(object):
    """
    Great article, explaining all needed algorithms https://www.redblobgames.com/pathfinding/a-star/introduction.html
    """

    EMPTY_SPACE = 0
    OBSTACLE = 1

    def __init__(self, maze: np.ndarray) -> None:
        """
        maze - a 2dim numpy array N by N, where 0 is empty space and 1 is a wall
        TODO: Maybe it should accept it as a graph?
        """
        super().__init__()

        assert maze is not None
        assert len(maze)
        assert maze.ndim == 2, 'Expect 2-dimentional numpy array as "maze" input!'
        assert maze.shape[0] == maze.shape[1], 'Maze should be a square!'

        self.maze = maze

    def _get_shortest_path_by_backward_traversal(self, came_from: Dict, finish: Point) -> List:
        assert finish in came_from, "Finish point wasn't visited (not in 'came_from' dict!"

        shortest_path_backwards = []
        point = finish
        while point in came_from:
            shortest_path_backwards.append(point)
            point = came_from[point]

        return list(reversed(shortest_path_backwards))

    def _is_inside_maze(self, p: Point) -> bool:
        row, col = p
        if row < 0 or col < 0:
            return False

        max_row, max_col = self.maze.shape
        if row >= max_row or col >= max_col:
            return False

        return True

    def _get_neighbours(self, p: Point) -> List[Point]:
        """Always expores neighnours in predefined order: right, down, left, up"""
        row, col = p
        neighbours = [(row, col+1), (row+1, col), (row, col-1), (row-1, col)]
        return [n for n in neighbours if self._is_inside_maze(n)]

    def _BFS(self, start: Point, finish: Point) -> List[Point]:
        assert self.maze[start[0]][start[1]] != self.OBSTACLE, "Start can't be an obstacle"
        assert self.maze[finish[0]][finish[1]] != self.OBSTACLE, "Finish can't be an obstacle"

        frontier_queue = []
        frontier_queue.append(start)
        came_from = dict()
        came_from[start] = None

        finish_found = False
        while frontier_queue:
            current = frontier_queue.pop(0)
            for neighbour in self._get_neighbours(current):
                # print(f'Exporing the neighbour {neighbour}')
                if neighbour in came_from:
                    # print(f'Already explored this guy {neighbour} -> skipping')
                    continue
                row, col = neighbour
                if self.maze[row][col] == self.OBSTACLE:
                    continue
                frontier_queue.append(neighbour)
                came_from[neighbour] = current

                if neighbour == finish:
                    # print(f'Finish {finish} found -> terminating the search')
                    finish_found = True
                    break

            if finish_found:
                break

        shortest_path = self._get_shortest_path_by_backward_traversal(came_from, finish)
        assert shortest_path[0] == start, 'Start point is not the first in the shortest path!'
        assert shortest_path[-1] == finish, 'Finish point is not the first in the shortest path!'

        return shortest_path


    def get_shortest_path(self, start: Point, finish: Point) -> Tuple[int, List]:
        distance, shortest_path = 0, []

        if start == finish:
            return (distance, shortest_path)

        shortest_path = self._BFS(start, finish)
        distance = len(shortest_path) - 1
        return (distance, shortest_path)

