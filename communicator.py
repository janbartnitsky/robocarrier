# simulates work of the solution
import sys

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

robots_count = 1
# print number of robots
sys.stdout.write(str(robots_count) + '\n')

# put first possible position for robot:
for i in range(0,map_name):
	j = citymap[i].find('.')
	if j != -1:
		break
sys.stdout.write(str(i+1) + ' ' + str(j+1) + '\n')
sys.stdout.flush()

# perform iterations
for _ in range(0, iterations_count):
	input_line = sys.stdin.readline()
	orders_in_iteration = int(input_line)
	for _ in range(0, orders_in_iteration):
		input_line = sys.stdin.readline()
		start_x, start_y, finish_x, finish_y = map(int, input_line.split())
	sys.stdout.write('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS\n')
	sys.stdout.flush()
