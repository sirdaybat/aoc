import sys

def split_to_groups(str):
	res = []
	while str:
		if str[0] == "[":
			e = str.find("]")
			res += [str[0:e+1]]
			str = str[e+1:]
		else:
			e = str.find("[")
			if e < 0:
				e = len(str)
			res += [str[0:e]]
			str = str[e:]
	return res

result = 0

for line in open(sys.argv[1], "rb"):
	if line.strip():
		groups = split_to_groups(line.strip())

		is_ok = False
		keep_going = True
		for g in groups:
			is_bracketed = g[0] == "["
			if is_bracketed:
				g = g[1:-1]
			for i in range(len(g)-4+1):
				s = g[i:i+4]
				if s[0] == s[3] != s[1] == s[2]:
					if is_bracketed:
						is_ok = False
						keep_going = False
						break
					else:
						is_ok = True
						break
			if not keep_going:
				break
		if is_ok:
			result += 1

print result

