import pandas as pd
import sys
import json

def convert_fr_dict(p):
	lines = []
	with open(p) as f:
		for line in f:
			if not line:
				continue
			if line[0] == '-':
				word = line[1:].strip()
				nextline = f.readline()
				if nextline.strip() == "-":
					continue
				lang = nextline.split('/')[0].strip()
				etymon = " ".join(nextline.split('/')[1:]).strip()
				normalized_etymon = etymon.split(",")[0]
				normalized_etymon = normalized_etymon.split("(")[0].strip()
				if " " in normalized_etymon:
					if normalized_etymon.split()[0] == "to":
						normalized_etymon = normalized_etymon.split()[1]
					else:
						print(normalized_etymon)
						normalized_etymon = normalized_etymon.split()[0]
				lines.append({"word": word, "source_language": lang, "raw_etymon": etymon,
					"etymon": normalized_etymon}) # TODO: better clean etymons
	df = pd.DataFrame.from_dict(lines)
	df.to_csv(p.split('.')[0] +".csv")

def convert_json_dict(p):
	lines = []
	with open(p) as f:
		contents = json.loads(f.read())
	for entry in contents['entries']:
		word = entry['word']
		for e in entry['etymologies']:
			lines.append({"word": word, "source_language": e['language'], "raw_etymon": e['rawEtymon'],
					"etymon": e['etymon']})
	df = pd.DataFrame.from_dict(lines)
	df.to_csv(p.split('.')[0] +".csv")

if __name__=="__main__":
	# convert_fr_dict(sys.argv[1])
	convert_json_dict(sys.argv[1])