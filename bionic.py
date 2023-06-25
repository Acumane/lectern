# Modified blixuk/bionic.py

F = 2.4 # fixation factor

def fixate(word: str) -> int:
	plain = ''.join(c for c in word if c.isalnum()) # remove punct.
	fixation = int(len(plain) / F)
	return fixation if fixation else 1

def bionify(word: str) -> str:
	if '-' in word:
		a, b = word.split('-')

		a = f"\033[01m{a[:fixate(a)]}\033[0m{a[fixate(a):]}"
		b = f"\033[01m{b[:fixate(b)]}\033[0m{b[fixate(b):]}"
		
		return f"{a}-{b}"
	else:
		return f"\033[01m{word[:fixate(word)]}\033[0m{word[fixate(word):]}"