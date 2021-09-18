#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import meta_path
import unittest

import numpy as np

from shortest_path_finder import ShortestPathFinder, convert_file_to_array_map



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

    def test_getting_correct_neighbours_on_the_start_edge_of_map(self):
        neighbours = self.spf._get_neighbours((0,0))
        expected_neighbours = [(0,1), (1,0)]
        self.assertEqual(neighbours, expected_neighbours)

    def test_getting_correct_neighbours_on_the_end_edge_of_map(self):
        neighbours2 = self.spf._get_neighbours((1,1))
        expected_neighbours2 = [(1,0), (0,1)]
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
        """
        [S ~ . .]
        [. F . .]
        [. . . .]
        [. . . .]
        """
        start = (0,0)
        finish = (1,1)
        dist, shortest_path = self.spf.get_shortest_path(start, finish)

        expected = (2, [start, (0,1), finish])
        self.assertEqual((dist, shortest_path), expected)

    def test_spf_finds_3_distance_straight_path(self):
        start = (3,3)
        finish = (0,3)
        dist, shortest_path = self.spf.get_shortest_path(start, finish)

        expected = (3, [start, (2,3), (1,3), finish])
        self.assertEqual((dist, shortest_path), expected)

    def test_spf_finds_distance_through_all_map(self):
        """
        [S ~ ~ ~]
        [. . . ~]
        [. . . ~]
        [. . . F]
        """
        start = (0,0)
        finish = (3,3)
        dist, shortest_path = self.spf.get_shortest_path(start, finish)

        expected = (6, [start, (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), finish])
        self.assertEqual((dist, shortest_path), expected)


class FileMapToArrayMapConverterTest(unittest.TestCase):
    def test_converting_4x4_empy_field(self):
        map4x4 = r'./maps/4'
        binary_map = convert_file_to_array_map(map4x4)
        expected_empty_field = np.zeros((4,4), dtype=int)

        np.testing.assert_array_equal(binary_map, expected_empty_field)

    def test_just_print_180x180_field_for_visual_comparison(self):
        map180x180 = r'./maps/180'
        binary_map = convert_file_to_array_map(map180x180)

        for l in binary_map:
            print(''.join([str(x) for x in l]))


class ShortestPathFinderOn180x180MazeTest(unittest.TestCase):
    def setUp(self):
        map180x180 = convert_file_to_array_map(r'./maps/180')
        print(map180x180[6])
        self.spf = ShortestPathFinder(map180x180)

    def test_trivial_0_distance_path(self):
        dist, shortest_path = self.spf.get_shortest_path((6,6), (6,6))

        self.assertEqual((dist, shortest_path), (0, []))

    def test_path_to_the_adjacent_empty_square(self):
        start = (3,3)
        finish = (3, 15)

        dist, shortest_path = self.spf.get_shortest_path(start, finish)
        print(f'Distance: {dist}, path: {shortest_path}')

        expected_dist = 3 + 12 + 3
        self.assertEqual(dist, expected_dist)


class ShortestPathFinderOn1000x1000MazeTest(unittest.TestCase):
    def setUp(self):
        map1000x1000 = convert_file_to_array_map(r'./maps/1000')
        print(map1000x1000[5])
        self.spf = ShortestPathFinder(map1000x1000)


    def test_long_path(self):
        start = (675,72)
        finish = (944, 876)

        dist, shortest_path = self.spf.get_shortest_path(start, finish)
        print(f'Distance: {dist}, {shortest_path}')

    def test_path_from_one_map_corner_to_another(self):
        start = (675,72)
        finish = (256, 848)

        dist, shortest_path = self.spf.get_shortest_path(start, finish)
        print(f'Distance: {dist}, path: {shortest_path}')



if __name__ == '__main__':
    unittest.main()
