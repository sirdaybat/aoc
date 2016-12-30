import sys
import re

nodedatamap = {}

for line in open(sys.argv[1], "rb"):
	line = line.strip()
	if not line:
		continue
	m = re.match(r"^/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T +(\d+)%$", line)
	if m:
		x, y, size, used, avail, usep = map(int, m.groups())
		assert used+avail == size
		nodedatamap[(x,y)] = [size,used]
		#print x, y, size, used, avail, usep

wid = 1 + max(x for (x,y) in nodedatamap)
hei = 1 + max(y for (x,y) in nodedatamap)

def printmap():
	for x in range(wid):
		line = ""
		for y in range(hei):
			line += "%2d/%2d " % (nodedatamap[(x,y)][1], nodedatamap[(x,y)][0])
		print line

import curses

printmap()

step = 0
while True:
	k = raw_input()
	off = None
	if k == "q":
		break
	elif k == "2":
		off = (1, 0)
	elif k == "8":
		off = (-1, 0)
	elif k == "6":
		off = (0, 1)
	elif k == "4":
		off = (0, -1)

	if not off:
		continue

	br = False
	ok = False
	for x in range(wid):
		for y in range(hei):
			if nodedatamap[(x,y)][1] == 0:
				br = True
				nx = x + off[0]
				ny = y + off[1]
				if (nx, ny) not in nodedatamap:
					print "BOUNDS"
					break
				if nodedatamap[(x,y)][0] < nodedatamap[(nx,ny)][1]:
					print "CAPACITY"
					break
				nodedatamap[(x,y)][1] = nodedatamap[(nx,ny)][1]
				nodedatamap[(nx,ny)][1] = 0
				ok = True
			if br: break
		if br: break

	if ok:
		step += 1
	printmap()
	print step

