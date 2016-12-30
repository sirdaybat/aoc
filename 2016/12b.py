import sys
import re

regs = {}
for reg in "abcd":
	regs[reg] = 0
regs["c"] = 1

commands = filter(None, map(str.strip, open(sys.argv[1], "rb").readlines()))

command_index = 0

while command_index < len(commands):
	line = commands[command_index]
	#print command_index, line, regs
	m = re.match(r"^cpy (.+) (.+)$", line)
	if m:
		src, dst = m.groups()
		src = regs[src] if src in regs else int(src)
		regs[dst] = src
	m = re.match(r"^inc (.+)$", line)
	if m:
		reg, = m.groups()
		regs[reg] += 1
	m = re.match(r"^dec (.+)$", line)
	if m:
		reg, = m.groups()
		regs[reg] -= 1
	m = re.match(r"jnz (.+) (.+)", line)
	if m:
		test, offset = m.groups()
		test = regs[test] if test in regs else int(test)
		offset = int(offset)
		if test != 0:
			command_index += offset - 1

	command_index += 1

print regs
