import edge_tts
from os.path import isfile
from collections import deque
from pathlib import Path
import prompts as p
import conf

rep = {
	'\n': ' ',
	'%¶%': '\n',
	'ﬁ': 'fi',
	'ﬀ': 'ff',
	'ﬂ': 'fl',
	'ﬃ': 'ffi',
}

async def synth(pg, text) -> None:
	AUDIO = f"page-{pg}.mp3"
	SUBS = f"page-{pg}"

	if isfile(f"page-{pg}.mp3"): # Skip if exists
		with open(SUBS, "r") as file:
			file.seek(0, 0)
			if file.readline() != "*": return

	if not text: # Skip if empty
		Path(SUBS).touch(); return

	prompt = p.SubMaker()
	communicate = edge_tts.Communicate(text, conf.VOICE, rate=conf.RATE)
	text = text.replace("\n\n", "%¶% ")
	prompt.puncted = deque(text.split())

	with open(AUDIO, "wb") as file:
		async for chunk in communicate.stream():
			if chunk["type"] == "audio":
				file.write(chunk["data"])
			elif chunk["type"] == "WordBoundary":
				prompt.times.append(chunk["offset"])
				prompt.plain.append(chunk["text"])

	with open(SUBS, "w", encoding="utf-8") as file:
		file.write(prompt.generate_subs())
		file.seek(0, 0)
		file.write("*")
	return

def clean(raw, pg):
	text = raw[pg-1].replace('\n\n', '%¶%') # preserve paragraphs
	for key, val in rep.items(): # Format + ligature fix
		text = text.replace(key, val)

	page = ""
	# Catch most headers, subtitles, & text fragments
	for line in text.splitlines():
		words = line.count(' ') + 1
		if words < 6: continue
		if words and words < 12 and line[-1] != '.': continue
		page += line.strip() + '\n\n'
	return page
