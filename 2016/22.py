import sys
import re

class node:
	def __init__(self, size, used, avail):
		self.size=size
		self.used=used
		self.avail=avail

nodes = {}

for line in open(sys.argv[1], "rb"):
	line = line.strip()
	if not line:
		continue
	m = re.match(r"^/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T +(\d+)%$", line)
	if m:
		x, y, size, used, avail, usep = map(int, m.groups())
		nodes[(x,y)] = node(size,used,avail)
		print x, y, size, used, avail, usep

viables = set()

for node in nodes:
	nodestate = nodes[node]
	if nodestate.used == 0:
		continue
	for onode in nodes:
		if onode == node:
			continue
		onodestate = nodes[onode]
		if nodestate.used <= onodestate.avail:
			print nodestate.used, onodestate.avail
			viables.add((node, onode))

print len(viables)
