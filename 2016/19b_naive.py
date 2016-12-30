import sys

num = int(sys.argv[1])

e = range(1, num+1)

"""

fwsize = 1
while fwsize < num:
	fwsize *= 2

fw = [0]*fwsize

print "fw size", fwsize

def fw_add(idx, val):
	idx += 1
	while idx < fwsize:
		fw[idx-1] += val
		idx += idx & -idx

def fw_getsum(idx):
	idx += 1
	res = 0
	while idx > 0:
		res += fw[idx-1]
		idx -= idx & -idx
	return res

for i in range(fwsize):
	fw_add(i, 1)

print "init done"

def fw_findsum(targetsum):
	lo = 0
	hi = fwsize-1
	while lo < hi:
		mid = (lo + hi) / 2
		s = fw_getsum(mid)
		if s < targetsum: lo = mid+1
		else: hi = mid
	assert lo == hi
	return lo

exists = [True]*num

remnum = num

while remnum > 1:
	i = 0
	while i < num:
		if not exists[i]:
			i += 1
			continue
		x = ((i+remnum)/2)%remnum+1
		a = fw_findsum(x)
		print x, a
		assert exists[a]
		exists[a] = False
		fw_add(a, -1)
		remnum -= 1
		i += 1

assert sum(exists) == 1
print exists.index(True)+1
"""

while len(e) > 1:
	i = 0
	while i < len(e):
		#print e[(i+len(e)/2)%len(e)]
		a = (i+len(e)/2)%len(e)
		print e[i], "steals at", a, "from", e[a], ".", i, len(e)
		assert a != i
		del e[a]
		if a > i:
			i += 1
		#print i, len(e)
	#print len(e)
print e

