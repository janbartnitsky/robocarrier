import io
import numpy as np
from PIL import Image

map_name = 1000

image_bytes = []
file_map = open('maps/' + str(map_name), 'r')
lines = file_map.readlines()
for line in lines:
	for position in range(0, len(line)):
		if line[position] == '.':
			image_bytes.append(255)
		elif line[position] == '#':
			image_bytes.append(0)
na = np.array(image_bytes, dtype=np.uint8)
im = Image.fromarray(na.reshape(map_name, map_name))
im.save(str(map_name)+'.bmp')

