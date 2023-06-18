import asyncio
from threading import Thread
from playsound import playsound
from collections import deque

# Function to convert timestamp into seconds
def convertTime(timestamp):
	hours, minutes, seconds = map(float, timestamp.split(':'))
	return hours * 3600 + minutes * 60 + seconds

async def printer(delay, caption, word):
	await asyncio.sleep(delay)
	if word == "%P%": print("\n", end="\t")
	else: print(word, end=' ', flush=True)

def play(pg):
	playsound(f'page-{pg}.mp3')

async def display(text, pg):
	text = text.replace("\n\n", " %P% ")
	words = deque(text.split())
	print("\t", end='')
	with open(f'page-{pg}.vtt', 'r') as f:
		next(f); next(f) # Skip first 2 lines
		tasks = []
		for line in f: # parsing VTT subtitles
			time, _ = line.split(' --> ')
			start = convertTime(time)
			caption = next(f).strip(); next(f)
			# next(f); next(f) # Skip to next timestamp
			tasks.append(printer(start, caption, words.popleft()))

		await asyncio.gather(*tasks)
