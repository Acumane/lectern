import pdftotext
import asyncio
from msspeech import MSSpeech

async def synth():
	mss = MSSpeech()
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

	filename = "output.mp3"
	print("\nSynthesizing...")
	await mss.synthesize(pages[28].strip(), filename)
	print("Done.")

with open("cosmos.pdf", "rb") as pdf:
	pages = pdftotext.PDF(pdf)

print(len(pages), "pages")
# print(pages[28])

asyncio.run(synth())