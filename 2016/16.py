import sys

def invert(s):
	return "".join("0" if c == "1" else "1" for c in s)

state = sys.argv[1].strip()
target_length = int(sys.argv[2])

while len(state) < target_length:
	state = state + "0" + invert(reversed(state))

state = state[:target_length]

while len(state) % 2 == 0:
	cs = ""
	for i in range(0, len(state), 2):
		cs += "01"[state[i] == state[i+1]]
	state = cs

print state
