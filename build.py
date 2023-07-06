import edge_tts
from collections import deque
import prompts as p

VOICE = "en-GB-SoniaNeural"
pages = {}

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

def clean(raw, first, last):
	for pg in range(first, last+1):
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
		pages[pg] = page
