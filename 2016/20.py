import sys
import re

segs = []

for line in open(sys.argv[1], "rb"):
	line = line.strip()
	if line:
		start, end = map(int, re.match(r"^(\d+)-(\d+)$", line).groups())
		segs.append((start, end))

best_pt = 2**32

def try_pt(x):
	global best_pt
	if x >= best_pt:
		return
	for seg in segs:
		if seg[0] <= x <= seg[1]:
			return
	best_pt = x

for seg in segs:
	if seg[0] > 0:
		try_pt(seg[0]-1)
	if seg[1] < 2**32-1:
		try_pt(seg[1]+1)

print best_pt
