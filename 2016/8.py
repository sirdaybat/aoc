import sys
import re

swid = 50
shei = 6

screen = [[0 for j in range(swid)] for i in range(shei)]

def ps():
	for y in range(shei):
		row = ""
		for x in range(swid):
			row += ".#"[screen[y][x]]
		print row
	print

for line in open(sys.argv[1], "rb"):
	line = line.strip()
	if line:
		ps()
		m = re.match(r"rect (.+)x(.+)", line)
		if m:
			w, h = map(int, m.groups())
			for y in range(h):
				for x in range(w):
					screen[y][x] = 1
			continue
		m = re.match(r"rotate column x=(.+) by (.+)", line)
		if m:
			x, amount = map(int, m.groups())
			while amount > 0:
				amount -= 1
				l = []
				for y in range(shei):
					l.append(screen[y][x])
				l = [l[-1]] + l[:-1]
				for y in range(shei):
					screen[y][x] = l[y]
			continue
		m = re.match(r"rotate row y=(.+) by (.+)", line)
		if m:
			y, amount = map(int, m.groups())
			while amount > 0:
				amount -= 1
				l = []
				for x in range(swid):
					l.append(screen[y][x])
				l = [l[-1]] + l[:-1]
				for x in range(swid):
					screen[y][x] = l[x]
			continue
		assert False

ps()

print sum(sum(l) for l in screen)
