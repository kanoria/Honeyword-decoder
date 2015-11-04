from constants import MAX_LEET_CHAR, LEET_REVERSE_MAPPER, ENGLISH_INDEX


def password_leaner(honeyword):
    """ Returns an understandable honeyword

    This function takes in a honeyword that can be 123pa$$w0rd45 and turns it
    into 123password45 The aim is to map l33t speak to real words so that we can
    work on the meaning instead of its written implementation
    """

    honeyword = honeyword.lower()

    # Replacing the characters in the honeyword by their leet equivalent
    linted_pass = ""
    for i in range(0, len(honeyword)):
        found_match = ""
        for j in range(1, MAX_LEET_CHAR):
            if honeyword[i:i+j] in LEET_REVERSE_MAPPER and len(found_match) < len(honeyword[i:i+j]):
                found_match = honeyword[i:i+j]

        if len(found_match) > 0:
            # In Leet speak to Latin char there are only 6 multiple mappings
            # for a character for simplification sake we only consider the
            # first and (for most chars) only one correspondence
            linted_pass = linted_pass + LEET_REVERSE_MAPPER[found_match][0]

        else:
            linted_pass = linted_pass + honeyword[i]

    # Finding the words inside the linted honeyword
    found_words = []
    for word, bool in ENGLISH_INDEX.iteritems():
        index = linted_pass.find(word)
        if index != -1 and len(word) > 0:
            if (index > 0 and not honeyword[index-1].isdigit() and not
                    honeyword[index].isdigit()) or index == 0:
                found_words.append({
                    "content": word,
                    "start_index": index,
                    "end_index": index + len(word) - 1
                })

    # Finding the words that are significant in the found words
    found_words = sorted(found_words, key=lambda k: k['start_index'])

    if len(found_words) == 0:
        return {
            "source_pass": honeyword,
            "mapped_pass": linted_pass,
            "tokens": {}
        }

    significant_words = [found_words[0]]
    pointer = 0

    for word in found_words:
        if significant_words[pointer]['start_index'] == word['start_index'] and significant_words[pointer]['end_index'] < word['end_index']:
            significant_words[pointer] = word
        elif significant_words[pointer]['end_index'] < word['start_index']:
            pointer += 1
            significant_words.append(word)

    # Putting all the results back together in the easy to read manner.
    output = ""
    pointer = 0
    last_word_end_index = 0
    for i in range(0, len(honeyword)):
        if pointer < len(significant_words) and i == significant_words[pointer]['start_index']:
            last_word_end_index = significant_words[pointer]['end_index']
            output = output + significant_words[pointer]['content']
            pointer += 1
        elif i > last_word_end_index:
            output = output + honeyword[i]

    # Returning the result in an output that can be used
    return {
        "source_pass": honeyword,
        "mapped_pass": output,
        "tokens": {
            "words": significant_words
        }
    }