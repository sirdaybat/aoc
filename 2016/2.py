import sys

def clamp(v):
	return max(0, min(2, v))

pos = (1, 1)

res = ""

for line in open(sys.argv[1], "rb"):
	if line.strip():
		for c in line.strip():
			if c == "U": pos = (pos[0], pos[1]-1)
			elif c == "D": pos = (pos[0], pos[1]+1)
			elif c == "L": pos = (pos[0]-1, pos[1])
			elif c == "R": pos = (pos[0]+1, pos[1])
			else: assert False
			pos = (clamp(pos[0]), clamp(pos[1]))
		#print pos
		res += ["123", "456", "789"][pos[1]][pos[0]]

print res
