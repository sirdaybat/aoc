import sys
import re

def expand(str):
	res = 0
	i = 0
	while i < len(str):
		if str[i] == "(":
			end = str.find(")", i)
			assert end >= 0
			desc = str[i+1 : end]
			m = re.match(r"^([\d]+)x([\d]+)$", desc)
			replen, numreps = map(int, m.groups())
			reppart = expand(str[end+1 : end+1+replen])
			res += numreps*reppart
			i = end+1+replen
		else:
			res += 1
			i += 1
	return res

line = open(sys.argv[1], "rb").readlines()[0]
line = line.strip()

#print line

res = ""

print expand(line)
"""
i = 0
while i < len(line):
	if line[i] == "(":
		end = line.find(")", i)
		if end >= 0:
			desc = line[i+1 : end]
			m = re.match(r"^([\d]+)x([\d]+)$", desc)
			replen, numreps = map(int, m.groups())
			reppart = line[end+1 : end+1+replen]
			res += numreps*reppart
			i = end+1+replen
		else:
			res += line[i]
			i += 1
	else:
		res += line[i]
		i += 1

#print res
print len(res)
"""
