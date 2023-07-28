import pdftotext
from os import mkdir, chdir
from itertools import cycle
from asyncio import run, create_task as start, sleep
from os.path import basename, splitext, isfile, exists
from build import clean, synth
from read import read
from sys import argv
import ansi as a

pages = {}
stopped = waiting = False

async def spin():
	print(end='\n', flush=True)
	spinner = cycle(['—', '/', '|', '\\'])
	while waiting:
		print(end=f"{a.I}{next(spinner)}{a.O}", flush=True)
		print(end='\b\b')
		await sleep(0.15)
	if not stopped:
		print(f"{a.I}\N{check mark}{a.O}")

async def main():
	if len(argv) != 3:
		print(f"{a.E}Insufficient arguments!\
		\nRequires a <path/to/*.pdf> and range: <first>-<last>")
		exit()

	path, selec = argv[1:]
	base = basename(path) 
	name, ext = splitext(base) 
	# speed = argv[4] if len(argv) > 3 else 1.0

	if ext != ".pdf":
		print(f"{a.E}File must be a PDF!"); exit()
	if not isfile(path):
		print(f"{a.E}File on path does not exist!"); exit()

	with open(path, "rb") as pdf:
		raw = pdftotext.PDF(pdf)

	first = last = 0;
	try:
		if '-' not in selec:
			first = last = int(selec)
		else: first, last = [int(x) for x in selec.split('-')]

		if last > len(raw) or first < 1 or last < 1:
			print(f"{a.E}Out of range! (1-{len(raw)})"); exit()
		if first > last:
			tmp = first; first = last; last = tmp

	except ValueError:
		print(f"{a.E}Pages must be positive integers!"); exit()
	
	if not exists(name): mkdir(name)
	chdir(name)

	for pg in range(first, last+1):
		pages[pg] = clean(raw, pg)

	# Request all pages concurrently; check on each via key	
	tasks = { 
		pg : start(synth(pg, text)) for pg, text in pages.items()
	}

	for pg in tasks:
		global stopped, waiting
		waiting = True
		if not stopped:
			spinner = start(spin())
			await tasks[pg]
			waiting = False; await spinner
			stopped = await read(pg)

	if stopped: print(f"\n{a.I}[QUIT]{a.O}")
	else: print(f"{a.I}[DONE]{a.O}")

if __name__ == "__main__":
	run(main())