import sys

num = int(sys.argv[1])

ll0 = [1, None, None]

lli = ll0

for i in range(1, num):
	lln = [i+1, lli, None]
	lli[2] = lln
	lli = lln

ll0[1] = lli
lli[2] = ll0


lli = ll0

for i in range(num/2):
	lli = lli[2]

remaining = num
while remaining > 1:
	#print "remove", lli[0]
	lli[1][2] = lli[2]
	lli[2][1] = lli[1]
	if remaining % 2 == 0:
		#print "go to prev"
		lli = lli[1]
	else:
		#print "go to next"
		lli = lli[2]
	lli = lli[2]

	remaining -= 1

print lli
