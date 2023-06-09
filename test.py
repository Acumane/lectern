import pdftotext
import asyncio
# import nltk
# nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from msspeech import MSSpeech

rep = {
	'\n': ' ',
	'ﬁ': 'fi',
	'ﬀ': 'ff'
}

async def setup():
	print("Fetching...")
	voices = await mss.get_voices_list()
	print("\nVoices:")
	for voice in voices:
		if voice["Locale"] == "en-US":
			print(voice["FriendlyName"].split(" ")[1], end=' ')
			print(voice["Gender"][0])
			await mss.set_voice(voice["Name"])

	await mss.set_rate(60)
	await mss.set_pitch(0)
	await mss.set_volume(1)

async def synth(p, n):
	output = f"{n:03}.mp3"
	await mss.synthesize(p.strip(), output)

	print('.', end='', flush=True)

with open("cosmos.pdf", "rb") as pdf:
	pages = pdftotext.PDF(pdf)

pRange = input(f"Pick reading range (1-{len(pages)}): ")
first, last  = [int(x)-1 for x in pRange.split('-')]

mss = MSSpeech()
asyncio.run(setup())
print("\nSynthesizing", end='')
for pg in range(first, last):
	sent = sent_tokenize(pages[pg])

	def correct(s, rep):
		return ''.join(rep.get(c, c) for c in s)

	clean = [correct(s, rep) for s in sent]

	# Combine sentences into groups of 5
	paras = (' '.join(clean[s:s+5]) for s in range(0, len(clean), 5))

	for n, p in enumerate(paras):
		asyncio.run(synth(p, n+1))

print("\nDone.")