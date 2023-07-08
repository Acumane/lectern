from bionic import bionify
from worker import Worker, sleep
from mpv import MPV
from os.path import getsize
from os import get_terminal_size
from collections import deque
from pynput.keyboard import Key, Listener
import ansi as a

cols, _ = get_terminal_size(0)
stopped = skipped = False
prompts = deque()
p = MPV()

def printer():
	global stopped, skipped
	print(end='\t')
	time, word = prompts.popleft()
	while True:
		sleep(0.01)
		if stopped: return
		if skipped:
			print(f"\t{a.I}[SKIPPED]{a.O}")
			skipped = False; return
		cur_time = p.time_pos
		if cur_time is None: continue

		if cur_time >= time:
			if "%¶%" in word: print(word[:-3], end='\n\n\t')
			else: print(bionify(word), end=' ', flush=True)
			if prompts:
				time, word = prompts.popleft()
			else: # End of page
				sleep(0.5) # Natural pause
				return

def parse(pg) -> bool:

	if not getsize(f'page-{pg}'): # Skip empty pages
		print(f"\t{a.I}[BLANK]{a.O}")
		return True

	prompts.clear()
	with open(f'page-{pg}', 'r') as file:
		next(file) # Skip file completion marker
		for time in file:
			word = next(file).strip(); next(file); next(file)
			prompts.append((float(time), word))
	return False

async def read(pg) -> bool:
	if stopped: return True
	print(f"{pg}", f"{a.S}⠀"*(cols-5), a.O, "\n")
	empty = parse(pg)
	if empty: return False

	t1 = Worker(p.play)
	t2 = Worker(printer)
	
	t1.start(f'page-{pg}.mp3'); t2.start()

	def press(key):
		global stopped, skipped
		if key == Key.space:
			p.pause = not p.pause
		if key == Key.esc:
			stopped = True; p.stop()
		if key == Key.enter:
			skipped = True; p.stop()
	l = Listener(on_press=press)
	l.start(); t1.join(); t2.join()

	return True if stopped else False

