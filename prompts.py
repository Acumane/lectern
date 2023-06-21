# (!) Substitute for submaker.py from edge-tts

import math
from collections import deque


def formatter(t: float, pl: str, pu: str) -> str:
	time = (t / 10**7)
	return (
		f"{time:.3f}\n"
		# f"{pl}\n"
		f"{pu}\n"
	)

class SubMaker:
	def __init__(self):
		self.times = []
		self.plain = deque()
		self.puncted = deque()

	def generate_subs(self) -> str:
		data = ""; nSkips = 0
		for t in self.times:
			pl = self.plain.popleft(); pu = "%NONE%"
			if nSkips: # Do the skipping
				nSkips -= 1
				continue
			if self.puncted:
				"""
				The way MS delimits "words" isn't only by whitespace. Two general cases: 
					1. "400 years" is one word, not two. So is "100 000 000 years"
					2. "1/2" becomes two words
				"""
				pu = self.puncted.popleft()
				unpu = ''.join(c for c in pu if c.isalnum()) # remove punct. for comparison
				if (pl != unpu):
					# print(f'\tInconsistent ("{pl}" vs. "{pu}")')
					group = pl.split()
					if len(group) > 1: # Case 1: many become one 
						for _ in group[1:]:
							pu += ' ' + self.puncted.popleft()
					# Case 2: one becomes many
					elif nSkips == 0:  # Find how many we must skip:
						next = ''.join(c for c in self.puncted[0] if c.isalnum())
						for i, pn in enumerate(self.plain, start=1):
							if pn == next:
								nSkips = i-1; break

			data += formatter(t, pl, pu) 

		return data
