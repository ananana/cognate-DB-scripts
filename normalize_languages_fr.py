import sys
import re

languages = {}
with open('langs_french_to_english.csv') as f:
	for line in f:
		lang1, lang2 = line.split(",")
		lang1 = lang1.strip()
		lang2 = lang2.strip()
		lang2 = re.sub("\\?", "", lang2)
		languages[lang1] = lang2

with open(sys.argv[1]) as f:
	for line in f:
		if not line.strip():
			print()
		elif line[0] == "-":
			print(line.strip())
		else:
			lang = line.split("/")[0]
			etymon = "/".join(line.split("/")[1:])
			if lang.strip() in languages:
				line = languages[lang.strip()] + " / " + etymon
			print(line.strip())
