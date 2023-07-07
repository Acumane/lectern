from bionic import bionify
from worker import Worker, sleep
import mpv
import os
from collections import deque
from pynput.keyboard import Key, Listener

cols, _ = os.get_terminal_size(0)
stop = skip = False
prompts = deque()
p = mpv.MPV()

def printer():
	global stop, skip
	print("\t", end='')
	time, word = prompts.popleft()
	while True:
		sleep(0.01)
		if stop: return
		if skip:
			print("\t\033[93m[SKIPPED]\033[0m")
			skip = False; return
		if p.time_pos is None: continue
		if p.time_pos >= time:
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

async def read(pg) -> bool:
	if stop: return False
	print(f"{pg}", "\033[9m⠀"*(cols-5), "\033[0m", "\n")
	parse(pg)

	t1 = Worker(p.play)
	t2 = Worker(printer)
	
	t1.start(f'page-{pg}.mp3'); t2.start()

	def press(key):
		global stop, skip
		if key == Key.space:
			p.pause = not p.pause
		if key == Key.esc:
			stop = True; p.stop()
		if key == Key.enter:
			skip = True; p.stop()
	l = Listener(on_press=press)
	l.start(); t1.join(); t2.join()

	return True

