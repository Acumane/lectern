# Modified blixuk/bionic.py
import ansi as a

F = 2.4 # fixation factor

def fixate(word: str) -> int:
	plain = ''.join(c for c in word if c.isalnum()) # remove punct.
	fixation = int(len(plain) / F)
	return fixation if fixation else 1

def bionify(word: str) -> str:
		parts = word.split('-')
		bolded = [f"{a.B}{p[:fixate(p)]}{a.O}{p[fixate(p):]}" for p in parts]
		return '-'.join(bolded)