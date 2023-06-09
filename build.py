import asyncio
import edge_tts

TEXT = """
This was nothing but a formality, instituted to reassure the masses, for the initiates
knew well enough that during his fast the artist would never in any circumstances, not
even under forcible compulsion, swallow the smallest morsel of food; the honor of his
profession forbade it.
"""

VOICE = "en-GB-SoniaNeural"
OUTPUT_FILE = "test.mp3"
WEBVTT_FILE = "test.vtt"


async def amain() -> None:
	communicate = edge_tts.Communicate(TEXT, VOICE, rate="+60%")
	submaker = edge_tts.SubMaker()
	with open(OUTPUT_FILE, "wb") as file:
		async for chunk in communicate.stream():
			if chunk["type"] == "audio":
				file.write(chunk["data"])
			elif chunk["type"] == "WordBoundary":
				submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

	with open(WEBVTT_FILE, "w", encoding="utf-8") as file:
		file.write(submaker.generate_subs(1))


loop = asyncio.get_event_loop_policy().get_event_loop()
try:
	loop.run_until_complete(amain())
finally:
	loop.close()
