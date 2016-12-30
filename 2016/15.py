import sys
import re

discs = []

for line in open(sys.argv[1], "rb"):
	line = line.strip()
	if line:
		m = re.match(r"^Disc #%d has (\d+) positions; at time=0, it is at position (\d+)\.$" % (len(discs)+1), line)
		numpos, initialpos = map(int, m.groups())
		discs.append((numpos, (initialpos+1+len(discs))%numpos))


print discs

maxd = max(discs, key=lambda v: v[0])

n = 0
while True:
	t = n*maxd[0] + (0 if maxd[1] == 0 else maxd[0]-maxd[1])
	if all((d[1]+t)%d[0] == 0 for d in discs):
		print t
		break
	n += 1
