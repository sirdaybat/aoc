import sys
import md5

result = ["."]*8
resultcount = 0

i = 0
while resultcount < 8:
	h = md5.md5(sys.argv[1] + str(i)).hexdigest()
	if h[:5] == "00000":
		pos = int(h[5], 16)
		if 0 <= pos < 8 and result[pos] == ".":
			result[pos] = h[6]
			resultcount += 1
			print "".join(result)
	i += 1

print "".join(result)
