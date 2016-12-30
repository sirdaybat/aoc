import sys
import md5

salt = sys.argv[1]

hashindex = 0
keys = []

hashmemo = {}
def gethash(i):
	if i in hashmemo:
		return hashmemo[i]

	h = md5.md5(salt + str(i)).hexdigest()
	for j in range(2016):
		h = md5.md5(h).hexdigest()
	hashmemo[i] = h
	return h

while len(keys) < 64:
	hash = gethash(hashindex)
	for i in range(len(hash)-3+1):
		c = hash[i]
		if c == hash[i+1] == hash[i+2]:
			found = False
			for j in range(1000):
				h = gethash(hashindex+1+j)
				for k in range(len(h)-5+1):
					if c == h[k] == h[k+1] == h[k+2] == h[k+3] == h[k+4]:
						keys.append(hashindex)
						found = True
						print hashindex, hashindex+1+j
						break
				if found:
					break
			break

	hashindex += 1

print keys, len(keys)
print hashindex-1
