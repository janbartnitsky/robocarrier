# chck robots position is valid for map 1000
import io
import numpy as np

map_name = 1000

image_bytes = []
file_map = open('maps/' + str(map_name), 'r')
lines = file_map.readlines()
for line in lines:
	for position in range(0, len(line)):
		if line[position] == '.':
			image_bytes.append(1)
		elif line[position] == '#':
			image_bytes.append(0)
na = np.array(image_bytes, dtype=np.uint8)
map_matrix = na.reshape(map_name, map_name)


robots_first_queue = [[234, 151], [244, 392], [282, 434], [359, 539], [359, 827], [383, 912], [437, 680], [446, 760], [500, 743], [515, 875], [342, 404], [426, 353], [391, 301], [477, 448], [448, 461], [396, 490], [512, 537], [482, 557], [443, 580], [600, 612], [531, 643], [652, 686], [649, 52], [704, 117], [760, 191], [825, 416], [934, 605], [904, 648], [751, 690], [854, 826], [897, 782]]

robots_second_queue = [[84, 236], [96, 235], [150, 298], [157, 294], [204, 355], [213, 355], [319, 237], [314, 341], [318, 348], [316, 492], [324, 489], [395, 610], [401, 606], [563, 723], [570, 725], [460, 258], [472, 260], [528, 219], [530, 227], [592, 176], [598, 181], [800, 271], [808, 272], [831, 338], [838, 337], [874, 474], [881, 477], [818, 642], [812, 652]]

for robot_position in robots_first_queue:
	if map_matrix[robot_position[0]][robot_position[1]] == 0:
		print("1 robot position is invalid")
		print(robot_position)

for robot_position in robots_second_queue:
	if map_matrix[robot_position[0]][robot_position[1]] == 0:
		print("2 robot position is invalid")
		print(robot_position)
