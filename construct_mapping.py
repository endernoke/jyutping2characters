import csv
import json
import os
import urllib.request
import tempfile

def download_file(url: str) -> str:
    """Download a file from URL and return its content as string."""
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

# URLs for the files
JYUTPING_TABLE_LIST_URL = 'https://raw.githubusercontent.com/lshk-org/jyutping-table/master/list.tsv'
RIME_ESSAY_URL = 'https://raw.githubusercontent.com/rime/rime-cantonese/main/essay-cantonese.txt'
RIME_DICT_URL = 'https://raw.githubusercontent.com/rime/rime-cantonese/main/jyut6ping3.words.dict.yaml'

all_jyutping_mapping = {}
chars_jyutping_mapping = {}

list_tsv_content = download_file(JYUTPING_TABLE_LIST_URL)
reader = csv.reader(reversed(list_tsv_content.splitlines()), delimiter='\t')
for row in reader:
    if len(row) < 3:
        # invalid schema
        continue
    chars_jyutping_mapping[row[0]] = row[2]
    all_jyutping_mapping[row[0]] = row[2]

def get_jyutping(phrase: str) -> str | None:
    jyutping = []
    for char in phrase:
        try:
            jyutping.append(chars_jyutping_mapping[char])
        except KeyError:
            print(f"Missing mapping for character: {char}")
            # skip this char
            return None
    return ''.join(jyutping)

word_frequencies_map = {}
essay_content = download_file(RIME_ESSAY_URL)
reader = csv.reader(essay_content.splitlines(), delimiter='\t')
for row in reader:
    if len(row) != 2:
        # invalid schema
        continue
    word_frequencies_map[row[0]] = int(row[1])
    word = row[0]
    jyutping = get_jyutping(word)
    if jyutping:
        all_jyutping_mapping[word] = jyutping

dict_content = download_file(RIME_DICT_URL)
tsv_content = dict_content[dict_content.index('...') + 3:].strip()
reader = csv.reader(reversed(tsv_content.splitlines()), delimiter='\t')
for row in reader:
    if len(row) < 2:
        # invalid schema
        continue
    # Ignore the x% column in the file because idk what it does lol
    word = row[0]
    jyutping = row[1].replace(' ', '') # remove whitespace delimiters
    if jyutping:
        all_jyutping_mapping[word] = jyutping

final_data = []
for word, jyutping in all_jyutping_mapping.items():
    frequency = word_frequencies_map.get(word, 0.1) # set to 0.1 in order to avoid division by zero later on
    final_data.append((word, jyutping, frequency))

with open("jyutping_mapping.json", "w") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"Data construction successful.\nTotal entries: {len(final_data)}")
