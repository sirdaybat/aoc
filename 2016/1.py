import sys

input = open(sys.argv[1], "rb").read()

parts = map(str.strip, input.split(","))

pos = (0, 0)
vec = (1, 0)

visited = set()
visited.add(pos)

for part in parts:
	dir = part[0]
	len = int(part[1:])
	
	if dir == "L":
		vec = (-vec[1], vec[0])
	else:
		assert dir == "R"
		vec = (vec[1], -vec[0])

	end = False
	for i in range(len):
		pos = (pos[0]+vec[0], pos[1]+vec[1])
		if pos in visited:
			end = True
			break
		visited.add(pos)
	if end:
		break

print abs(pos[0]) + abs(pos[1])
