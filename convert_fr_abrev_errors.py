import json
import re

with open("abrevieri-fr.json") as f:
	abrevieri = json.loads(f.read())

abbrev_keys = list(abrevieri.keys())

for k in abbrev_keys:
	# include version without .s, each subword in turn
	for i, w in enumerate(k.split()):
		new_key = k.split()
		new_key[i] = re.sub("\.", "", new_key[i])
		abrevieri[" ".join(new_key)] = abrevieri[k]
	abrevieri[re.sub("\.", "", k)] = abrevieri[k]
# sort in descending order of number of words in the abbreviation,
# and secondly by length 
# that way more complex ones get expanded first
abbrev_keys = list(abrevieri.keys())
# abbrev_keys = sorted(abbrev_keys, key=lambda w: -len(w.split()))
abbrev_keys = sorted(abbrev_keys, key=lambda w: -len(w))

with open("french_mistakes.log") as f:
	for line in f:
		split_line = line.split()
		word = split_line[0]
		definition = " ".join(split_line[3:])
		new_words = []
		found = False
		for k in abbrev_keys:
			if definition.find(k + " ")>=0 and not found:
				definition = re.sub(k, abrevieri[k] + " / ", definition)
				
				# Uncomment to output new terms 
				print(word)
				print(definition.strip())
				found = True
				print()
				
				continue
		# Uncomment to log errors:
		# if not found:
			# print(word, "NOT FOUND", definition)
			# print("-")
		# print()