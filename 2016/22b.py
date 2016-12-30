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
		nodedatamap[(x,y)] = (size,used)
		#print x, y, size, used, avail, usep

wid = 1 + max(x for (x,y) in nodedatamap)
hei = 1 + max(y for (x,y) in nodedatamap)

def nodeindex((x,y)):
	return y*wid+x

coords = [(x,y) for y in range(hei) for x in range(wid)]

nodesizes = []
for c in coords:
	nodesizes.append(nodedatamap[c][0])

inodeuseds = []
for c in coords:
	inodeuseds.append(nodedatamap[c][1])

print coords
print nodesizes
print inodeuseds

for c in coords:
	ci = nodeindex(c)
	print nodesizes[ci], inodeuseds[ci], nodedatamap[c]
	assert nodesizes[ci] == nodedatamap[c][0] and inodeuseds[ci] == nodedatamap[c][1]

inodeuseds=tuple(inodeuseds)
istate = (wid-1, inodeuseds)

offsets = ((1, 0),1), ((-1, 0),-1), ((0, 1),wid), ((0, -1),-wid)

istatelinks = set()
for c in coords:
	ci = nodeindex(c)
	if inodeuseds[ci] == 0:
		continue
	for (offset, indexoffset) in offsets:
		nc = (c[0]+offset[0], c[1]+offset[1])
		if not (0<=nc[0]<wid and 0<=nc[1]<hei):
			continue
		nci = ci + indexoffset
		if not (inodeuseds[ci] <= nodesizes[nci]-inodeuseds[nci]):
			continue
		istatelinks.add((ci, nci))

queue = [(istate, (istatelinks,))]
visited = {istate}
#vh = {hash(istate)}
step = 0

while queue:
	step += 1
	newqueue = []
	for (state, (statelinks,)) in queue:
		#print state
		at = state[0]
		nodeuseds = state[1]
		for ci, nci in statelinks:
			#for (offset,indexoffset) in offsets:
			#	nc = (c[0]+offset[0], c[1]+offset[1])
			#	if not (0<=nc[0]<wid and 0<=nc[1]<hei):
			#		continue
			#	nci = ci + indexoffset

			#assert nci == nodeindex(nc)
			#nci = nodeindex(nc)
			if not (nodeuseds[ci] <= nodesizes[nci]-nodeuseds[nci]):
				continue
			nat = at if ci != at else nci
			if nat == 0:
				print "ANKKA", step
				exit(1)
			nnodeuseds = list(nodeuseds)
			nnodeuseds[nci] += nnodeuseds[ci]
			nnodeuseds[ci] = 0
			nnodeuseds = tuple(nnodeuseds)
			nstate = (nat, nnodeuseds)
			#hns = hash(nstate)
			#if hns in vh:
			#	continue
			#vh.add(hns)
			if nstate in visited:
				continue
			visited.add(nstate)

			nistatelinks = set()
			for a,b in statelinks:
				if nnodeuseds[a] == 0:
					continue
				if not (nnodeuseds[a] <= nodesizes[b]-nnodeuseds[b]):
					continue
				nistatelinks.add((a,b))
			a=ci
			ax, ay = a%wid, a/wid
			for (offset,indexoffset) in offsets:
				bx = ax+offset[0]
				by = ay+offset[1]
				if not (0<=bx<wid and 0<=by<hei):
					continue
				b = a+indexoffset
				if not (nnodeuseds[b] <= nodesizes[a]):
					continue
				nistatelinks.add((b,a))

			newqueue.append((nstate,(nistatelinks,)))
				#else:
				#	print "cannot", (x,y), "to", (nbx,nby), "(", sg[y][x].used, sg[nby][nbx].avail, ")"
	queue = newqueue
	print len(queue)

print step
