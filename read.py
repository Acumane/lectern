import asyncio
from bionic import bionify
from playsound import playsound

async def printer(delay, word):
	await asyncio.sleep(delay)
	if "%¶%" in word: print(word[:-3], end='\n\n\t')
	else: print(bionify(word), end=' ', flush=True)

def play(pg):
	playsound(f'page-{pg}.mp3')

async def display(pg):
	print("\t", end='')
	with open(f'page-{pg}', 'r') as f:
		tasks = []
		for time in f:
			word = next(f).strip();
			tasks.append(printer(float(time), word))

	await asyncio.gather(*tasks)
