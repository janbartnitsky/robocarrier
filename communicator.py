#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# simulates work of the solution
import sys
import random

# return from 1 to 100 robots
def how_many_robots_to_use(map_name, cost_courier, iterations_count, orders_count):
	return 1

# unassign order from robot
def stop_order(order):
	pass

# return moves from path
def get_robot_path_for_iteration(robot):
	if len(robot["path"]) < 60:
		return_path = robot["path"] + ("S" * (60 - len(robot["path"])))
		robot["path"] = ""
	else:
		return_path = robot["path"][0:60]
		robot["path"] = robot["path"][60:]
	return return_path

# get test conditions
input_line = sys.stdin.readline()
map_name, max_tips, cost_courier = map(int, input_line.split())

# skip map details
citymap = []
for _ in range(0,map_name):
	input_line = sys.stdin.readline()
	citymap.append(input_line)

# get iterations and orders count
input_line = sys.stdin.readline()
iterations_count, orders_count = map(int, input_line.split())

# decide how many robots we need
robots_count = how_many_robots_to_use(map_name, cost_courier, iterations_count, orders_count)
sys.stdout.write(str(robots_count) + '\n')

# define robots position
if map_name == 1000:
	robots_initial_positions = [[396, 490], [477, 448], [448, 461], [482, 557], [751, 690], [512, 537], [500, 743], [359, 539], [426, 353], [652, 686], [443, 580], [342, 404], [897, 782], [359, 827], [437, 680], [446, 760], [282, 434], [244, 392], [531, 643], [600, 612], [854, 826], [704, 117], [904, 648], [391, 301], [383, 912], [515, 875], [825, 416], [234, 151], [934, 605], [649, 52], [760, 191], [84, 236], [96, 235], [150, 298], [157, 294], [204, 355], [213, 355], [319, 237], [314, 341], [318, 348], [316, 492], [324, 489], [395, 610], [401, 606], [563, 723], [570, 725], [460, 258], [472, 260], [528, 219], [530, 227], [592, 176], [598, 181], [800, 271], [808, 272], [831, 338], [838, 337], [874, 474], [881, 477], [818, 642], [812, 652], [396, 490], [477, 448], [448, 461], [482, 557], [751, 690], [512, 537], [500, 743], [359, 539], [426, 353], [652, 686], [443, 580], [342, 404], [897, 782], [359, 827], [437, 680], [446, 760], [396, 490], [477, 448], [448, 461], [482, 557], [751, 690], [512, 537], [500, 743], [359, 539], [426, 353], [652, 686], [443, 580], [342, 404], [897, 782], [359, 827], [437, 680], [446, 760], [282, 434], [244, 392], [531, 643], [600, 612], [854, 826], [396, 490], [477, 448], [448, 461], [482, 557]]
	robots_set = [{"position": robots_initial_positions[i], "assigned_order": -1} for i in range(robots_count)]
else:
	robots_set = []
	while len(robots_set) < robots_count:
		x_coord, y_coord = random.randint(1, map_name), random.randint(1, map_name - 1)
		if citymap[x_coord][y_coord] == '.':
			robots_set.append({"position": [x_coord, y_coord], "assigned_order": None, "path": ""})
			# output robot's positions
			sys.stdout.write(str(x_coord) + ' ' + str(y_coord) + '\n')
sys.stdout.flush()

orders_set = [] # [{"start": [1, 1], "finish": [1, 1], "max_possible_tips": max_tips} for i in range(robots_count)]

# perform iterations
for _ in range(0, iterations_count):
	input_line = sys.stdin.readline()
	orders_in_iteration = int(input_line)
	# append new orders to orders set
	for _ in range(0, orders_in_iteration):
		input_line = sys.stdin.readline()
		start_x, start_y, finish_x, finish_y = map(int, input_line.split())
		orders_set.append({"start": [start_x, start_y], "finish": [finish_x, finish_y], "max_possible_tips": max_tips, "responsible_robot": -1})

	# update max possible tips for each order in the list AKA protuhanie
	order_number = 0
	for order in orders_set:
		order_number += 1
		order["max_possible_tips"] -= 60
		# remove order from set if there is no chance for tips for it anymore
		if order["max_possible_tips"] <= 0:
			orders_set.remove(order)

	# do all the magic: dispatch robots for orders and assign action pathes


	for robot in robots_set:
		robot_path = get_robot_path_for_iteration(robot)
		sys.stdout.write(robot_path + '\n')

	sys.stdout.flush()
