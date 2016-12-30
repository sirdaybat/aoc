import sys
import re

regs = {}
for reg in "abcd":
        regs[reg] = 0

regs["a"] = 12

commands = filter(None, map(str.strip, open(sys.argv[1], "rb").readlines()))

command_index = 0

step = 0

max_command_index = -1

while command_index < len(commands):
	max_command_index = max(max_command_index, command_index)

	if commands[command_index : command_index+6] == ["cpy b c", "inc a", "dec c", "jnz c -2", "dec d", "jnz d -5"]:
		assert regs["b"] != 0
		print "ankka", regs["b"], regs["d"]
		regs["a"] += regs["b"]*regs["d"]
		regs["c"] = 0
		regs["d"] = 0
		command_index += 6
	else:
		line = commands[command_index]

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
				print "TOGGLE", step, idx
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

	if step>1000000:
		print commands
		print command_index
		print regs
		print
	elif step%100000 == 0:
		print commands
		print step, "...", regs

	step += 1
	
print step
print regs
