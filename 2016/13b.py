import sys

favnum = int(sys.argv[1])

startpos = (1,1)
visited = {startpos}
queue = [startpos]

def num_ones(v):
	res = 0
	while v:
		res += 1
		v &= v-1
	return res

def is_free_pos((x,y)):
	return x >= 0 and y >= 0 and num_ones((x*x + 3*x + 2*x*y + y + y*y) + favnum) % 2 == 0

assert is_free_pos(startpos)

step = 0
while step < 50:
	newqueue = []
	for pos in queue:
		for off in ((1, 0), (-1, 0), (0, 1), (0, -1)):
			newpos = (pos[0]+off[0], pos[1]+off[1])
			if not is_free_pos(newpos):
				continue
			if newpos in visited:
				continue
			visited.add(newpos)
			newqueue.append(newpos)
	queue = newqueue
	step += 1

print step, len(visited)

"""
for y in range(7):
	l = ""
	for x in range(10):
		l += "#."[is_free_pos((x,y))]
	print l

"""
