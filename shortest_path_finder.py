#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
I'm trying to use TDD here
"""

from typing import Dict, List, Tuple
from unittest.result import TestResult

import numpy as np

Point = Tuple

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
        print(f"Here's our maze:\n{maze}")

    def _get_shortest_path_by_backward_traversal(self, came_from: Dict, finish: Point) -> List:
        assert finish in came_from, "Finish point wasn't visited (not in 'came_from' dict!"

        shortest_path_backwards = []
        point = finish
        while point in came_from:
            shortest_path_backwards.append(point)
            point = came_from[point]

        return list(reversed(shortest_path_backwards))

    def _is_inside_maze(self, p: Point) -> bool:
        px, py = p
        if px < 0 or py < 0:
            return False

        max_x, max_y = self.maze.shape
        if px >= max_x or py >= max_y:
            return False

        return True

    def _get_neighbours(self, p: Point) -> List[Point]:
        """Always expores neighnours in predefined order: right, down, left, up"""
        px, py = p
        neighbours = [(px+1, py), (px, py+1), (px-1, py), (px, py-1)]
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
                print(f'Exporing the neighbour {neighbour}')
                if neighbour in came_from:
                    print(f'Already explored this guy {neighbour} -> skipping')
                    continue
                nx, ny = neighbour
                if self.maze[nx][ny] == self.OBSTACLE:
                    continue
                frontier_queue.append(neighbour)
                came_from[neighbour] = current

                if neighbour == finish:
                    print(f'Finish {finish} found -> terminating the search')
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

