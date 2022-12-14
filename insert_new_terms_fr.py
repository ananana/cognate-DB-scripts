import sys
from collections import OrderedDict


def read_dict_contents(filepath):
	definitions = OrderedDict()
	with open(filepath) as f:
		contents = f.read()
	for par in contents.split("\n\n"):
		if not par:
			continue
		word = par.split("\n")[0]
		try:
			definition = par.split("\n")[1]
			definitions[word] = definition
		except:
			print("ERROR: could not split", par)
	return definitions

old_dict = read_dict_contents(sys.argv[1])
new_dict = read_dict_contents(sys.argv[2])

old_dict.update(new_dict)

for w in old_dict:
	print(w)
	print(old_dict[w])
	print()