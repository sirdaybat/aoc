import sys

arr = []

for line in open(sys.argv[1], "rb"):
	nums = line.split()
	if len(nums) == 3:
		nums = map(int, nums)
		arr.append(nums)

assert len(arr) % 3 == 0

result = 0

for i in range(0, len(arr), 3):
	for j in range(3):
		t = [arr[i][j], arr[i+1][j], arr[i+2][j]]
		t = sorted(t)
		if t[0]+t[1]>t[2]:
			result += 1

print result
