#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import numpy as np

from shortest_path_finder import ShortestPathFinder


class ShortestPathFinderTest(unittest.TestCase):
    def get_2x2_maze(self):
        return np.zeros((2,2), dtype=int)

    def setUp(self):
        a_maze = self.get_2x2_maze()
        self.spf = ShortestPathFinder(a_maze)

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

    def test_spf_same_start_finish(self):
        start = (0,0)
        finish = (0,0)
        dist, shortest_path = self.spf.get_shortest_path(start, finish)

        self.assertEqual((dist, shortest_path), (0, []))

    def test_getting_correct_neighbours_on_the_edge_of_map(self):
        neighbours = self.spf._get_neighbours((0,0))
        expected_neighbours = [(1,0), (0,1)]
        self.assertEqual(neighbours, expected_neighbours)

        neighbours2 = self.spf._get_neighbours((1,1))
        expected_neighbours2 = [(0,1), (1,0)]
        self.assertEqual(neighbours2, expected_neighbours2)

    def test_spf_finds_1_distance_path(self):
        start = (0,0)
        finish = (1,0)
        dist, shortest_path = self.spf.get_shortest_path(start, finish)

        expected = (1, [start, finish])
        self.assertEqual((dist, shortest_path), expected)


class ShortestPathFinderOn4x4MazeTest(unittest.TestCase):
    def get_4x4_maze(self):
        return np.zeros((4,4), dtype=int)

    def setUp(self):
        a_maze = self.get_4x4_maze()
        self.spf = ShortestPathFinder(a_maze)

    def test_spf_finds_2_distance_path(self):
        start = (0,0)
        finish = (1,1)
        dist, shortest_path = self.spf.get_shortest_path(start, finish)

        expected = (2, [start, (1,0), finish])
        self.assertEqual((dist, shortest_path), expected)

    def test_spf_finds_3_distance_straight_path(self):
        start = (3,3)
        finish = (0,3)
        dist, shortest_path = self.spf.get_shortest_path(start, finish)

        expected = (3, [start, (2,3), (1,3), finish])
        self.assertEqual((dist, shortest_path), expected)

    def test_spf_finds_distance_through_all_map(self):
        start = (0,0)
        finish = (3,3)
        dist, shortest_path = self.spf.get_shortest_path(start, finish)

        expected = (6, [start, (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), finish])
        self.assertEqual((dist, shortest_path), expected)


if __name__ == '__main__':
    unittest.main()
