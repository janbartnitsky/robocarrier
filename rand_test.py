# how to generate number of orders for each iteration
import random

map_name, max_tips, cost_courier, iterations_count, orders_count = 384, 500, 1000, 100, 100

# get a list of allowed coordinates for a given map
allowed_coordinates = []
file_map = open('maps/' + str(map_name), 'r')
lines = file_map.readlines()
line_num = 0
for line in lines:
	for position in range(0, len(line)):
		if line[position] == '.':
			allowed_coordinates.append([line_num, position])
	line_num += 1

# create a set of iterations
iterations_set = [[] for i in range(iterations_count)]

# randomly create start and finish points for each order and assign it to a random iteration
for _ in range(1, orders_count):
	random_iteration_number = random.randint(0, iterations_count - 1)
	iterations_set[random_iteration_number].append([random.choice(allowed_coordinates), random.choice(allowed_coordinates)])

# simulate test performance
print(str(map_name) + ' ' + str(max_tips) + ' ' + str(cost_courier))
for line in lines:
	print(line[0:-1])
print(str(iterations_count) + ' ' + str(orders_count))
for iteration in iterations_set:
	print(len(iteration))
	for order in iteration:
		print(str(order[0][0]) + ' ' + str(order[0][1]) + ' ' + str(order[1][0]) + ' ' + str(order[1][1]))
