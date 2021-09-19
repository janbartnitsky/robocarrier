#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# simulates work of the solution

import sys
import random

import numpy as np


# ===========================================================================================================

from typing import Dict, List, Tuple
from unittest.result import TestResult

Point = Tuple

def convert_path_to_string(shortest_path: List[Point]) -> str:
	if not shortest_path:
		return ''

	assert len(shortest_path) >= 2, f'Minimum path should be of length 2 ({len(shortest_path)} was provided)!'
	res = []
	for i in range(0, len(shortest_path)-1):
		# define path from robot to order start (+ take order)

		# define path from order start to finish (+ put order)

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


# ===========================================================================================================

test_run = True # rename to false before Submit
skip_prod_tests = [180, 384, 1024, 1000]

# return from 1 to 100 robots
def how_many_robots_to_use(map_name, cost_courier, iterations_count, orders_count):
	return 1

# return moves from path
def get_robot_path_for_iteration(robot):
	order_finished = False
	if len(robot["path"]) < 60:
		return_path = robot["path"] + ("S" * (60 - len(robot["path"])))
		robot["path"] = ""
		order_finished = True
	else:
		return_path = robot["path"][0:60]
		robot["path"] = robot["path"][60:]
	return return_path, order_finished

# get test conditions
if test_run:
	map_name, max_tips, cost_courier, iterations_count, orders_count = 1024, 3600, 555555, 50000, 75259
	print("TEST:", map_name, max_tips, cost_courier, iterations_count, orders_count)
else:
	input_line = sys.stdin.readline()
	map_name, max_tips, cost_courier = map(int, input_line.split())


if test_run:
	allowed_coordinates = []
	file_map = open('maps/' + str(map_name), 'r')
	lines = file_map.readlines()
	line_num = 0
	for line in lines:
		for position in range(0, len(line)):
			if line[position] == '.':
				allowed_coordinates.append([line_num + 1, position + 1])
		line_num += 1

	# create a set of iterations
	iterations_set = [[] for i in range(iterations_count)]


# skip map details
citymap = []
for i in range(0,map_name):
	if test_run:
		input_line = lines[i]
		#print("TEST:", input_line)
	else:
		input_line = sys.stdin.readline()
	for position in range(0, len(input_line)):
		if input_line[position] == '.':
			citymap.append(0)
		elif input_line[position] == '#':
			citymap.append(1)
citymap = np.array(citymap, dtype=int)
citymap = citymap.reshape(map_name, map_name)

spf = ShortestPathFinder(citymap)

# get iterations and orders count
if not test_run:
	input_line = sys.stdin.readline()
	iterations_count, orders_count = map(int, input_line.split())
else:
	# randomly create start and finish points for each order and assign it to a random iteration
	for _ in range(1, orders_count):
		random_iteration_number = random.randint(0, iterations_count - 1)
		iterations_set[random_iteration_number].append([random.choice(allowed_coordinates), random.choice(allowed_coordinates)])



# decide how many robots we need
robots_count = 1#how_many_robots_to_use(map_name, cost_courier, iterations_count, orders_count)
sys.stdout.write(str(robots_count) + '\n')
sys.stdout.flush()


# define robots position
robots_set = []
while len(robots_set) < robots_count:
	row, col = random.randint(0, map_name - 1), random.randint(0, map_name - 1)
	if citymap[row][col] == 0:
		robots_set.append({"position": (row, col), "path": ""})

# output robot's positions
for robot in robots_set:
	sys.stdout.write(str(robot["position"][0] + 1) + ' ' + str(robot["position"][1] + 1) + '\n')
sys.stdout.flush()
# print(f'[D] all robots: {robots_set}')


orders_set = [] # [{"start": [1, 1], "finish": [1, 1], "max_possible_tips": max_tips} for i in range(robots_count)]

# perform iterations
for i in range(0, iterations_count):
	if test_run:
		orders_in_iteration = len(iterations_set[i])
		print("TEST:", orders_in_iteration)
	else:
		input_line = sys.stdin.readline()
		orders_in_iteration = int(input_line)
	# append new orders to orders set
	for j in range(0, orders_in_iteration):
		if test_run:
			order = iterations_set[i][j]
			start_x, start_y, finish_x, finish_y = order[0][0], order[0][1], order[1][0], order[1][1]
			print("TEST:", start_x, start_y, finish_x, finish_y)
		else:
			input_line = sys.stdin.readline()
			start_x, start_y, finish_x, finish_y = map(int, input_line.split())
		orders_set.append({"start": (start_x-1, start_y-1), "finish": (finish_x-1, finish_y-1), "max_possible_tips": max_tips, "responsible_robot": -1})

	# print(f'[D] all orders: {orders_set}')
	robot = robots_set[0]

	# if robot is free
	if robot["path"] == "" and len(orders_set) > 0:
		orders_set = sorted(orders_set, key=lambda x: x['max_possible_tips'], reverse=True)
		current_order = orders_set.pop(0)

		if test_run == True or map_name not in skip_prod_tests:

			full_robot_path = ''
			dist, path = spf.get_shortest_path(robot['position'], current_order['start'])
			path_to_the_package = convert_path_to_string(path)
			full_robot_path += path_to_the_package
			full_robot_path += 'T'
			dist, path = spf.get_shortest_path(current_order['start'], current_order['finish'])
			path_to_the_drop_point = convert_path_to_string(path)
			full_robot_path += path_to_the_drop_point
			full_robot_path += 'P'

			robot["path"] = full_robot_path

	for robot in robots_set:
		robot_path, order_finished = get_robot_path_for_iteration(robot)
		#error check: robot position must be in the place of finished order
		if order_finished:
			robot["position"] = current_order['finish']
			if test_run:
				if robot["position"] != current_order["finish"]:
					print("Something wrong with the order ", robot["position"], current_order["finish"])
		sys.stdout.write(robot_path + '\n')
	sys.stdout.flush()

	# update max possible tips for each order in the list AKA protuhanie
	order_number = 0
	for order in orders_set:
		order_number += 1
		order["max_possible_tips"] -= 60
		# remove order from set if there is no chance for tips for it anymore
		if order["max_possible_tips"] <= 0:
			orders_set.remove(order)
