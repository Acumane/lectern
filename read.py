import asyncio
from threading import Thread
from playsound import playsound

# Function to convert timestamp into seconds
def convertTime(timestamp):
	hours, minutes, seconds = map(float, timestamp.split(':'))
	return hours * 3600 + minutes * 60 + seconds

async def printer(delay, caption):
	await asyncio.sleep(delay)
	print(caption, end=' ', flush=True)

def play(n):
	playsound(f'page-{n}.mp3')

async def display(n):
	with open(f'page-{n}.vtt', 'r') as f:
		next(f); next(f) # Skip first 2 lines
		tasks = []
		for line in f:
			_, time = line.split(' --> ')
			start = convertTime(time)
			caption = next(f).strip(); next(f)
			tasks.append(printer(start, caption))

		await asyncio.gather(*tasks)
