# Defaults:
VOICE = "en-US-AriaNeural"
RATE = "+50%"
BIONIC = NEW = True

def toPerc(c: float) -> str:
	perc = int((c - 1) * 100)
	return f"{'+' if perc >= 0 else '-'}{abs(perc)}%"

with open("lec.conf", "r") as conf:
	for line in conf:
		# Skip comments and empty lines:
		if not line.strip() or line.strip().startswith("#"): continue
		pref, val = [x.strip() for x in line.split("=")]
		if pref == "voice": VOICE = val	
		elif pref == "rate": RATE = toPerc(float(val))
		elif pref == "bionic":
			BIONIC = True if val.title() == "True" else False
		elif pref == "welcome":
			NEW = True if val.title() == "True" else False
	
	print(f"Using voice {VOICE} at {RATE} speed.")
