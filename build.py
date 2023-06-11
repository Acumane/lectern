import pdftotext
import asyncio
import edge_tts
from os.path import isfile
from threading import Thread
from read import play, display

VOICE = "en-GB-SoniaNeural"

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

#change

loop = asyncio.get_event_loop_policy().get_event_loop()
try:
	print("Synthesizing:")
	for pg in range(first, last+1):
		if isfile(f"page-{pg}.mp3"):
			print(f"   #{pg}    *")
			continue
		loop.run_until_complete(synth(pages[pg-1], pg))
	for pg in range(first, last+1):
		print(f"\n\n{pg}", "—"*60, "\n")
		threads = []
		threads.append(Thread(target=play, args=(pg,) ))
		threads.append(Thread(target=asyncio.run, args=(display(pg), ) ))
		
		for t in threads: t.start() # Start both threads
		for t in threads: t.join()  # Wait for them (page) to finish

finally:
	loop.close()
