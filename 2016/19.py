import sys

num = int(sys.argv[1])

e = range(1, num+1)

#print e

while len(e) > 1:
	i = 0
	while i < len(e):
		if e[i] == -1:
			i += 1
			continue
		e[(i+1)%len(e)] = -1
		i += 1
	e = filter(lambda x: x != -1, e)
print e
