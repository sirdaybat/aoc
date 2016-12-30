import sys
import md5

result = ""

i = 0
while len(result) < 8:
	h = md5.md5(sys.argv[1] + str(i)).hexdigest()
	if h[:5] == "00000":
		result += h[5]
		print result
	i += 1

print result
