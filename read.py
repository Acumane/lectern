from bionic import bionify
from worker import Worker, sleep
from playsound import playsound
import mpv

prompts = []
p = mpv.MPV() # terminal=True

def printer():
	print("\t", end='')
	for delay, _, word in prompts:
		sleep(delay)
		if "%¶%" in word: print(word[:-3], end='\n\n\t')
		else: print(bionify(word), end=' ', flush=True)

def parse(pg):
	prompts.clear()
	with open(f'page-{pg}', 'r') as file:
		prev: float = 0.0
		for time in file:
			word = next(file).strip();
			prompts.append((float(time) - prev, float(time), word))
			prev = float(time)



def read(pg):
	print(f"\n\n{pg}", "\033[9m⠀"*75, "\033[0m", "\n")
	parse(pg)

	t1 = Worker(playsound)
	t2 = Worker(printer)
	
	t1.start(f'page-{pg}.mp3'); t2.start()
	# Play/pause demo:
	# sleep(5)
	# p.pause = not p.pause; t2.pause()
	# sleep(2)
	# p.pause = not p.pause; t2.resume()	
	t1.join(); t2.join()

# @p.on_key_press('q')
# def pause():
# 	p.pause = not p.pause;
