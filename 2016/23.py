import sys
import re

regs = {}
for reg in "abcd":
	regs[reg] = 0

regs["a"] = 7

commands = filter(None, map(str.strip, open(sys.argv[1], "rb").readlines()))

command_index = 0

step = 0

while command_index < len(commands):
	line = commands[command_index]
	#print command_index, line, regs
	m = re.match(r"^cpy (.+) (.+)$", line)
	if m:
		src, dst = m.groups()
		src = regs[src] if src in regs else int(src)
		assert dst in regs
		regs[dst] = src
	m = re.match(r"^inc (.+)$", line)
	if m:
		reg, = m.groups()
		assert reg in regs
		regs[reg] += 1
	m = re.match(r"^dec (.+)$", line)
	if m:
		reg, = m.groups()
		assert reg in regs
		regs[reg] -= 1
	m = re.match(r"jnz (.+) (.+)", line)
	if m:
		test, offset = m.groups()
		test = regs[test] if test in regs else int(test)
		offset = regs[offset] if offset in regs else int(offset)
		if test != 0:
			command_index += offset - 1
	m = re.match(r"tgl (.+)", line)
	if m:
		offset, = m.groups()
		offset = regs[offset] if offset in regs else int(offset)
		idx = command_index + offset
		if idx < len(commands):
			pre = commands[idx][:3]
			post = commands[idx][3:]
			if pre == "jnz":
				pre = "cpy"
			elif pre == "cpy":
				pre = "jnz"
			elif pre == "inc":
				pre = "dec"
			elif pre in ("dec", "tgl"):
				pre = "inc"
			else:
				assert False
			commands[idx] = pre + post

	command_index += 1

	if step%100000 == 0:
		print step, "...", regs

	step += 1

print regs
