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

def get_xyxs_in_str(str):
	result = []
	for i in range(len(str)-3+1):
		s = str[i : i+3]
		if s[0] == s[2] != s[1]:
			result.append(s)
	return result

def get_xyxs_in_strs(strs):
	result = []
	for str in strs:
		result += get_xyxs_in_str(str)
	return result

result = 0

for line in open(sys.argv[1], "rb"):
	if line.strip():
		groups = split_to_groups(line.strip())

		groups_a = [g[1:-1] for g in groups if g[0] == "["]
		groups_b = [g for g in groups if g[0] != "["]

		#print groups_a
		#print groups_b

		xsa = get_xyxs_in_strs(groups_a)
		xsb = get_xyxs_in_strs(groups_b)

		#print xsa
		#print xsb

		for xa in xsa:
			if xa[1] + xa[0] + xa[1] in xsb:
				#print "*"
				result += 1
				break

print result

