newlangs = []
with open('langs_french_to_english.csv') as f:
	for line in f:
		if line[0] == " ":
			newlangs.append(line.strip().split(",")[1])

ordered_langs = []
with open('Tabel-limbi-sursa.csv') as f:
	for line in f:
		ordered_langs.append(",".join(line.strip().split(",")[1:]))

for lang in set(newlangs):
	if lang == "?":
		continue
	ordered_langs.append(",,,," + lang)

print("0," + ordered_langs[0])
i = 1
for lang in sorted(ordered_langs[1:], key=lambda l: l.strip(",")):
	print(",".join([str(i),lang]))
	i = i+1