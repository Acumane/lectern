import pdftotext
import asyncio
import sys
import edge_tts
from read import read
from os.path import isfile
from collections import deque
import prompts as p

VOICE = "en-GB-SoniaNeural"

rep = {
	'\n': ' ',
	'%¶%': '\n',
	'ﬁ': 'fi',
	'ﬀ': 'ff',
	'ﬂ': 'fl',
	'ﬃ': 'ffi',
}

async def synth(text, n) -> None:
	OUTPUT = f"page-{n}.mp3"
	SUBS = f"page-{n}"
	prompt = p.SubMaker()
	communicate = edge_tts.Communicate(text, VOICE, rate="+60%")
	text = text.replace("\n\n", "%¶% ")
	prompt.puncted = deque(text.split())
	print(f"   #{n}...", end=' ', flush=True)
	with open(OUTPUT, "wb") as file:
		async for chunk in communicate.stream():
			if chunk["type"] == "audio":
				file.write(chunk["data"])
			elif chunk["type"] == "WordBoundary":
				prompt.times.append(chunk["offset"])
				prompt.plain.append(chunk["text"])

	with open(SUBS, "w", encoding="utf-8") as file:
		file.write(prompt.generate_subs())
	print("\N{check mark}")

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("\033[91mInsufficient arguments!\nRequires a <path/to/*.pdf> and range: <first>-<last>")
		exit()
	path, pRange = sys.argv[1:]
	# speed = sys.argv[4] if len(sys.argv) > 3 else 1.0
	
	with open(path, "rb") as pdf:
		pages = pdftotext.PDF(pdf)

	first, last  = [int(x) for x in pRange.split('-')]

	selec = {}
	for pg in range(first, last+1):
		text = pages[pg-1].replace('\n\n', '%¶%') # preserve paragraphs
		for key, val in rep.items(): # Format + ligature fix
			text = text.replace(key, val)

		clean = ""
		# Catch most headers, subtitles, & text fragments
		for line in text.splitlines():
			words = line.count(' ') + 1
			if words < 6: continue
			if words and words < 12 and line[-1] != '.': continue
			clean += line.strip() + '\n\n'
		selec[pg] = clean


	loop = asyncio.get_event_loop_policy().get_event_loop()
	try:
		print("Synthesizing:")
		for pg, text in selec.items():
			if isfile(f"page-{pg}.mp3"):
				print(f"   #{pg}    *")
				continue
			loop.run_until_complete(synth(text, pg))
		for pg, text in selec.items():
			# print(text)
			read(pg)

	finally:
		loop.close()
