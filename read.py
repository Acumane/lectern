import asyncio
from threading import Thread
from playsound import playsound as play

# Function to convert timestamp into seconds
def convertTime(timestamp):
	hours, minutes, seconds = map(float, timestamp.split(':'))
	return hours * 3600 + minutes * 60 + seconds

async def display(delay, caption):
	await asyncio.sleep(delay)
	print(caption, end=' ', flush=True)

async def main():
	with open('test.vtt', 'r') as f:
		next(f); next(f) # Skip first 2 lines
		tasks = []
		for line in f:
			time, _ = line.split(' --> ')
			start = convertTime(time)
			caption = next(f).strip(); next(f)
			tasks.append(display(start, caption))

		await asyncio.gather(*tasks)

# play('test.mp3')
Thread(target=play, args=('test.mp3',) ).start()
asyncio.run(main())
