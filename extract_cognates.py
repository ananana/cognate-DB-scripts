import pandas as pd
import numpy as np
from unidecode import unidecode
import sys

SOURCE_LANGS_FILE = "Tabel-limbi-sursa3.0.csv"

def get_dict_filename(lang):
	return f'{lang}-12-12.csv'

def get_source_languages(lang):
	langs_header = {
		'portuguese': 'PG',
		'spanish': 'SP',
		'italian': 'IT',
		'romanian': 'RO',
		'french': 'FR'
	}

	df = pd.read_csv(SOURCE_LANGS_FILE, sep=",")
	df = df.fillna('')

	source_langs = df[langs_header[lang]].values
	return [normalize_lang(l) for l in (filter(None, source_langs))]

def languages_match(slang1, slang2, lang1, lang2):
	return slang1.split()[:2]==slang2.split()[:2] # TODO: make this more sophisticated

def etymons_match(etymon1, etymon2):
	return unidecode(etymon1.split()[0]) == unidecode(etymon2.split()[0])

def normalize_etymon(etymon):
	return unidecode(str(etymon))
	# return unidecode(str(etymon).split()[0])

def normalize_lang(lang):
	if lang in 'dial.Abruzzo/dial.arabian/dial.Emilia/dial.Genoa/dial.Lucca/dial.Milano/dial.northern.Italy/dial.Piemont/dial.Puglia/dial.Roma/dial.Romagna/dial.Toscana/dial.Trento/dial.Trieste'.split('/'):
		lang = 'dialectal italian'
	if 'latin' in str(lang).split():
		return 'latin'  # TODO: improve
	if 'provençal' in str(lang).split():
		return unidecode('provençal')
	if 'francique' in str(lang).split():
		return 'frankish'
	return unidecode(" ".join(str(lang).split()[:2]))

def extract_cognates(lang1, lang2):
	filename1 = get_dict_filename(lang1)
	filename2 = get_dict_filename(lang2)

	df1 = pd.read_csv(filename1, dtype={'word': str, 'source_language': str, 'etymon': str, 'raw_etymon': str})
	words1 = df1.to_dict(orient='index')
	df2 = pd.read_csv(filename2, dtype={'word': str, 'source_language': str, 'etymon': str, 'raw_etymon': str})
	words2 = df2.to_dict(orient='index')

	langs1 = get_source_languages(lang1)
	langs2 = get_source_languages(lang2)

	cognates = []
	etymon_langs1 = {}
	etymon_langs2 = {}

	for k1 in words1:
		
		word1 = words1[k1]['word']
		slang1 = words1[k1]['source_language']
		etymon1 = words1[k1]['etymon']
		etymon_langs1[(
			normalize_etymon(etymon1),
			normalize_lang(slang1))] = word1
		if normalize_lang(slang1) not in langs1:
			print(k1,slang1, "is not standard.")
	for k2 in words2:
		word2 = words2[k2]['word']
		slang2 = words2[k2]['source_language']
		etymon2 = words2[k2]['etymon']
		if normalize_lang(slang2) not in langs2:
			print(k2,slang2, "is not standard.")
		etymon_langs2[(
			normalize_etymon(etymon2),
			normalize_lang(slang2))] = word2
	for el in etymon_langs1:
		if el in etymon_langs2:
			etymon, slang = el
			if slang in [lang1, lang2]:
				continue # skip borrowings
			if str(slang) == 'nan' or str(etymon) == 'nan':
				continue
		# if languages_match(slang1, slang2, lang1, lang2) and etymons_match(etymon1, etymon2):
			cognates.append({f'word_{lang1}': etymon_langs1[el], f'word_{lang2}': etymon_langs2[el], 
				'etymon': etymon, 
				'source_language': slang})
	df_cognates = pd.DataFrame.from_dict(cognates)
	df_cognates.to_csv(f'cognates_{lang1}_{lang2}-12-12.csv')


if __name__=="__main__":
	# print(get_source_languages('portuguese'))
	extract_cognates(sys.argv[1], sys.argv[2])



