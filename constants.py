import json

# Files
__ENGLISH_DICTIONARY_FILE__ = './resources/englishWords.txt'
__LEET_MAP_FILE__ = './resources/leetMap.json'

# Key is a word so that looking in the dictionary is 0(1)
ENGLISH_INDEX = {}

""" Loads the english dictionary into an index with the key as words
"""
with open(__ENGLISH_DICTIONARY_FILE__) as f:
    for word in f:
        ENGLISH_INDEX[word[:-1]] = True

""" Loads the mapper into memory
"""
with open(__LEET_MAP_FILE__) as data_file:
    # Maps a latin character to a leet character (can be several keyboard characters)
    LEET_MAPPER = json.load(data_file)


""" Generates the reverse mapper from the leet speak map
"""
# maximun number of characters for a leet character
MAX_LEET_CHAR = 0
# Maps a Leet character (can be several keyboards characters) to a latin character
LEET_REVERSE_MAPPER = {}

for letter, charList in LEET_MAPPER.iteritems():
    for char in charList:
        if char in LEET_REVERSE_MAPPER:
            LEET_REVERSE_MAPPER[char].append(letter)
        else:
            LEET_REVERSE_MAPPER[char] = [letter]

        if len(char) > MAX_LEET_CHAR:
            MAX_LEET_CHAR = len(char)