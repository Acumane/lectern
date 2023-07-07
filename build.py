import edge_tts
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

async def synth(pg, text) -> None:
	if isfile(f"page-{pg}.mp3"): return
	OUTPUT = f"page-{pg}.mp3"
	SUBS = f"page-{pg}"
	prompt = p.SubMaker()

	communicate = edge_tts.Communicate(text, VOICE, rate="+60%")
	text = text.replace("\n\n", "%¶% ")
	prompt.puncted = deque(text.split())

	with open(OUTPUT, "wb") as file:
		async for chunk in communicate.stream():
			if chunk["type"] == "audio":
				file.write(chunk["data"])
			elif chunk["type"] == "WordBoundary":
				prompt.times.append(chunk["offset"])
				prompt.plain.append(chunk["text"])

	with open(SUBS, "w", encoding="utf-8") as file:
		file.write(prompt.generate_subs())
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
