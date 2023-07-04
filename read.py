from bionic import bionify
from worker import Worker, sleep
import mpv
from collections import deque
from pynput.keyboard import Key, Listener

prompts = deque()
p = mpv.MPV()

def printer():
	print("\t", end='')
	time, word = prompts.popleft()
	while True:
		sleep(0.01)
		if p.playback_time >= time:
			if "%¶%" in word: print(word[:-3], end='\n\n\t')
			else: print(bionify(word), end=' ', flush=True)
			if prompts:
				time, word = prompts.popleft()
			else: # End of page
				sleep(0.5) # Natural pause
				return

def parse(pg):
	prompts.clear()
	with open(f'page-{pg}', 'r') as file:
		prev: float = 0.0
		for time in file:
			word = next(file).strip(); next(file); next(file)
			prompts.append((float(time), word))
			prev = float(time)

def read(pg):
	print(f"\n\n{pg}", "\033[9m⠀"*75, "\033[0m", "\n")
	parse(pg)

	t1 = Worker(p.play)
	t2 = Worker(printer)
	
	t1.start(f'page-{pg}.mp3'); t2.start()

	def press(key):
		if key == Key.space:
			p.pause = not p.pause

	l = Listener(on_press=press)
	l.start(); t1.join(); t2.join()

