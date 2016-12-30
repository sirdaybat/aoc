import sys

num = int(sys.argv[1])

e = range(1, num+1)

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
			#print i+1, "dead"
			i += 1
			continue
		index_of_current_elf = fw_getsum(i)-1
		index_of_other_elf = (index_of_current_elf+remnum/2)%remnum
		value_of_other_elf = fw_findsum(index_of_other_elf+1)
		#print x, a
		#print x, a+1
		#print i+1, "steals at", index_of_other_elf, "from", value_of_other_elf+1, ". ", index_of_current_elf, remnum
		assert exists[value_of_other_elf]
		exists[value_of_other_elf] = False
		fw_add(value_of_other_elf, -1)
		remnum -= 1
		i += 1
		if i%10000 == 0:
			print "(%d)" % i
	print remnum

assert sum(exists) == 1
print exists.index(True)+1

"""
while True:

while len(e) > 1:
	i = 0
	while i < len(e):
		#print e[(i+len(e)/2)%len(e)]
		del e[(i+len(e)/2)%len(e)]
		i += 1
		#print i, len(e)
	#print len(e)
print e
"""
