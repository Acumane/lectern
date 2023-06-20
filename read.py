import asyncio
from threading import Thread
from playsound import playsound
from collections import deque

# Function to convert timestamp into seconds
def convertTime(timestamp):
	hours, minutes, seconds = map(float, timestamp.split(':'))
	return hours * 3600 + minutes * 60 + seconds

async def printer(delay, word):
	await asyncio.sleep(delay)
	if word == "%P%": print("\n", end="\t")
	else: print(word, end=' ', flush=True)

def play(pg):
	playsound(f'page-{pg}.mp3')

async def display(text, pg):
	pass # out of commision!
	# text = text.replace("\n\n", " %P% ")
	# words = deque(text.split())
	# # print(text)
	# print("\t", end='')
	# with open(f'page-{pg}', 'r') as f:
	# 	tasks = []
	# 	for time in f:
	# 		start = convertTime(time)
	# 		tasks.append(printer(start, words.popleft()))

	# 	await asyncio.gather(*tasks)
