import pdftotext
import asyncio
import edge_tts
from os.path import isfile
from threading import Thread
from read import play, display

VOICE = "en-GB-SoniaNeural"

rep = {
	'\n': ' ',
	'%P%': '\n',
	'ﬁ': 'fi',
	'ﬀ': 'ff',
	'ﬃ': 'ffi',
}

async def synth(text, n) -> None:
	OUTPUT = f"page-{n}.mp3"
	SUBS = f"page-{n}.vtt"
	submaker = edge_tts.SubMaker()
	communicate = edge_tts.Communicate(text, VOICE, rate="+60%")
	print(f"   #{n}...", end=' ', flush=True)
	with open(OUTPUT, "wb") as file:
		async for chunk in communicate.stream():
			if chunk["type"] == "audio":
				file.write(chunk["data"])
			elif chunk["type"] == "WordBoundary":
				submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

	with open(SUBS, "w", encoding="utf-8") as file:
		file.write(submaker.generate_subs(1))
	print("\N{check mark}")

with open("cosmos.pdf", "rb") as pdf:
	pages = pdftotext.PDF(pdf)

pRange = input(f"Pick reading range (1-{len(pages)}): ")
first, last  = [int(x) for x in pRange.split('-')]

selec = {}
for pg in range(first, last+1):
	text = pages[pg-1].replace('\n\n', '%P%') # preserve paragraphs
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
		print(f"\n\n{pg}", "—"*60, "\n")
		threads = []
		threads.append(Thread(target=play, args=(pg,) ))
		threads.append(Thread(target=asyncio.run, args=(display(text, pg), ) ))
		
		for t in threads: t.start() # Start both threads
		for t in threads: t.join()  # Wait for them (page) to finish

finally:
	loop.close()
