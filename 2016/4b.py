import sys
import re
from collections import Counter

input = open(sys.argv[1], "rb")

result = 0

for line in input:
	if line.strip():
		m = re.match(r"(.*)-([^-]*)\[(.*)\]", line.strip())
		name, id, check = m.groups()

		def shift(c):
			if c.isalpha():
				return chr(((ord(c)-ord("a"))+int(id))%(ord("z")-ord("a")+1)+ord("a"))
			else:
				return c

		name = "".join(shift(c) for c in name)
		print name, id

		"""
		assert len(check) == 5
		assert all(c.isdigit() for c in id)
		counts = Counter([c for c in name if c.isalpha()])
		def compare(a,b):
			diff = b[1]-a[1]
			if diff != 0: return diff
			return ord(a[0])-ord(b[0])
		mc = "".join([v[0] for v in sorted(list(counts.iteritems()), cmp=compare)])
		if check == mc[:5]:
			result += int(id)
		"""

print result
