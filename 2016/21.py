import sys
import re

str = list(sys.argv[2])

for line in open(sys.argv[1], "rb"):
	line = line.strip()
	if not line:
		continue
	ok = False
	m = re.match(r"^swap position (\d+) with position (\d+)$", line)
	if m:
		a, b = map(int, m.groups())
		ok = True
		t = str[a]
		str[a] = str[b]
		str[b] = t
	m = re.match(r"^swap letter (.) with letter (.)$", line)
	if m:
		a, b = m.groups()
		ok = True
		str = [b if c == a else a if c == b else c for c in str]
	m = re.match(r"^reverse positions (\d+) through (\d+)$", line)
	if m:
		a, b = map(int, m.groups())
		ok = True
		str[a:b+1] = reversed(str[a:b+1])
	m = re.match(r"^rotate (left|right) (\d+) step.?$", line)
	if m:
		dir = -1 if m.groups()[0] == "left" else 1
		steps = int(m.groups()[1])
		ok = True
		if dir < 0:
			for i in range(steps):
				str = str[1:] + str[:1]
		else:
			for i in range(steps):
				str = str[-1:] + str[:-1]
	m = re.match(r"^rotate based on position of letter (.)$", line)
	if m:
		letter = m.groups()[0]
		ok = True
		idx = str.index(letter)
		assert idx >= 0
		steps = 1 + idx + (1 if idx >= 4 else 0)
		for i in range(steps):
			str = str[-1:] + str[:-1]
	m = re.match(r"^move position (\d+) to position (\d+)$", line)
	if m:
		a, b = map(int, m.groups())
		ok = True
		c = str.pop(a)
		str.insert(b, c)

	if not ok:
		print list(line)
		assert False
	print str

print "".join(str)
