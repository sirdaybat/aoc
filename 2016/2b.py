import sys

def clamp(v):
	return max(0, min(4, v))

map = [
"..1..",
".234.",
"56789",
".ABC.",
"..D.."
]

pos = (0, 2)

res = ""

for line in open(sys.argv[1], "rb"):
	if line.strip():
		for c in line.strip():
			prevpos = pos
			if c == "U": pos = (pos[0], pos[1]-1)
			elif c == "D": pos = (pos[0], pos[1]+1)
			elif c == "L": pos = (pos[0]-1, pos[1])
			elif c == "R": pos = (pos[0]+1, pos[1])
			else: assert False
			pos = (clamp(pos[0]), clamp(pos[1]))
			if map[pos[1]][pos[0]] == ".": pos = prevpos
		#print pos
		res += map[pos[1]][pos[0]]

print res
