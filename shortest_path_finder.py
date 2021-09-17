#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
I'm trying to use TDD here
"""

from typing import List, Tuple
import unittest

import numpy as np

class ShortestPathFinder(object):
    """
    https://www.redblobgames.com/pathfinding/a-star/introduction.html ?
    """
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


    def get_shortest_path(self, start: Tuple, finish: Tuple):
        pass

class ShortestPathFinderTest(unittest.TestCase):
    def get_4x4_maze(self):
        return np.zeros((4,4), dtype=int)

    def test_spf_asserts_on_invalid_input_maze(self):
        with self.assertRaises(AssertionError):
            empty_maze = []
            ShortestPathFinder(empty_maze)

        with self.assertRaises(AssertionError):
            one_dimentional_array = np.array([1,2,3])
            ShortestPathFinder(empty_maze)

    def test_spf_accepts_two_dimensional_array_on_creation(self):
        valid_maze = np.array([[0,0], [0,1]])
        spf = ShortestPathFinder(valid_maze)

    def test_spf_finds_some_path_on_simplest_maze(self):
        simplest_maze = self.get_4x4_maze()
        spf = ShortestPathFinder(simplest_maze)

        start = (0,0)
        finish = (2,2)
        shortest_path = spf.get_shortest_path(start, finish)
        self.assertIsNotNone(shortest_path)


if __name__ == '__main__':
    unittest.main()
