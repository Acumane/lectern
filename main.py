import asyncio
import pdftotext
from os.path import basename, splitext, isfile
from build import clean, pages, synth
from read import read
import sys

done = False

def main():
	if len(sys.argv) != 3:
		print("\033[91mInsufficient arguments!\nRequires a <path/to/*.pdf> and range: <first>-<last>")
		exit()

	path, selec = sys.argv[1:]
	base = basename(path) 
	name, ext = splitext(base) 
	# speed = sys.argv[4] if len(sys.argv) > 3 else 1.0

	if not isfile(path):
		print("\033[91mFile on path does not exist!"); exit()
	if ext != ".pdf":
		print("\033[91mFile must be a PDF!"); exit()

	with open(path, "rb") as pdf:
		raw = pdftotext.PDF(pdf)

	first = last = 0;
	try:
		if '-' not in selec:
			first = last = int(selec)
		else: first, last = [int(x) for x in selec.split('-')]

		if last > len(raw) or first < 1 or last < 1:
			print(f"\033[91mOut of range! (1-{len(raw)})"); exit()
		if first > last:
			tmp = first; first = last; last = tmp

	except ValueError:
		print("\033[91mPages must be positive integers!"); exit()

	clean(raw, first, last)
	loop = asyncio.get_event_loop_policy().get_event_loop()
	try:
		print("Synthesizing:")
		for pg, text in pages.items():
			if isfile(f"page-{pg}.mp3"):
				print(f"   #{pg}    *")
				continue
			loop.run_until_complete(synth(text, pg))

	finally:
		loop.close()

	for pg in pages:
		global done; done = read(pg)
	
	if done: print("\n\033[93m[DONE]\033[0m")
	else: print("\n\033[93m[QUIT]\033[0m")


if __name__ == "__main__":
	main()