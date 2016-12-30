import sys

result = 0

for line in open(sys.argv[1], "rb"):
	nums = line.split()
	if len(nums) == 3:
		nums = map(int, nums)
		nums = sorted(nums)
		if nums[0] + nums[1] > nums[2]:
			result += 1
print result

