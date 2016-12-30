import sys
import re

segs = []

for line in open(sys.argv[1], "rb"):
	line = line.strip()
	if line:
		start, end = map(int, re.match(r"^(\d+)-(\d+)$", line).groups())
		seg = (start, end)
		segs.append(seg)

while True:
	foo = False
	i = 0
	while i < len(segs):
		#print i
		a = segs[i]
		j = i+1
		while j < len(segs):
			b = segs[j]
			if a[1] >= b[0] and b[1] >= a[0]:
				segs[i] = (min(a[0], b[0]), max(a[1], b[1]))
				segs.pop(j)
				foo = True
				break
			j += 1
		if foo:
			break
		i += 1
	if not foo:
		break

for seg in segs:
	for oseg in segs:
		if seg == oseg:
			continue
		if seg[1] >= oseg[0] and oseg[1] >= seg[0]:
			assert False

def seglen(seg):
	return seg[1]-seg[0]+1

print segs

print len(segs)
print sum(map(seglen, segs))
print 2**32 - sum(map(seglen, segs))
