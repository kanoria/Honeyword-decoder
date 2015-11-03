import pprint

pp = pprint.PrettyPrinter(indent=1)

def isInAlphabeticalSequence(word):
    """
    Checks if the string passed to it is in an alphabetical sequence
    """
    if len(word) == 1:
        return False
    else:
        for i in range(len(word) - 1):
            if ord(word[i]) != ord(word[i + 1]) + 1:
                return False
        return True


def isInReverseAlphabeticalSequence(word):
    """
    Checks if the string passed to it is in a reverse alphabetical sequence
    """
    if len(word) == 1:
        return False
    else:
        for i in range(len(word) - 1):
            if ord(word[i]) != ord(word[i + 1]) - 1:
                return False
        return True


def isSameCharacterSequence(word):
    """
    Checks if the string passed to it is in a sequence of identical characters
    """
    if len(word) == 1:
        return False
    else:
        for i in range(len(word) - 1):
            if word[i] != word[i + 1]:
                return False
        return True


def isOnlySpecialCharacters(word):
    """
    Checks if the string passed is comprised entirely of special characters typically allowed in passwords
    """
    for i in range(len(word)):
        if word[i].isalpha() or word[i].isdigit():
            return False
    return True


def isInSequence(word):
    """
    Checks if the string passed is a sequence of digits logically connected ("e.g. 369")
    """
    if len(word)<3:
        return False
    else:
        increment = int(word[0]) - int(word[1])
        for i in range(len(word) - 2):
            if int(word[i+1]) - int(word[i+2]) != increment:
                return False
        return True


def classifyCharacter(word):
    """
    Classifies the passed single character string into an alphabet, number, or special character
    """
    if word[0].isalpha():
        return "isalpha"
    elif word[0].isalpha():
        return "isdigit"
    else:
        return "isspecialchar"


def classifier(token):
    """ Classifies the given token into one of several categories.
    categories currently defined are:
        same_sequence_letters: same letter being repeated (e.g. "aaa")
        sequence_letters: letters in alphabetical sequence or reverse alphabetical sequence (e.g. "abc", "zyx")
        random_letters: string of random letters (e.g. dyumd)
        same_sequence_numbers: same digit being repeated (e.g. "22222")
        sequence_numbers: logical sequence of digits (e.g. "369")
        even_numbers: all digits are even digits (e.g. "4824")
        odd_numbers: all digits are odd digits (e.g. "35573")


    Classifies by priority:
    words: constant sequence > sequence > random
    numbers: constant sequence > sequence > odd or even > random numbers
    special chars: constant sequence > random
    """

    #check if token is a string of alphabets


    if token.isalpha():
        #check if token is a sequence of the same alphabet:
        if isSameCharacterSequence(token):
            return "same_sequence_letters"
        elif isInAlphabeticalSequence(token) or isInReverseAlphabeticalSequence(token):
            return "sequence_letters"
        else:
            return "random_letters"

    #check if token is a number
    elif token.isdigit():
        if isSameCharacterSequence(token):
            return "same_sequence_numbers"
        elif isInSequence(token):
            return "sequence_numbers"
        else:
            evenCount = 0
            oddCount = 0
            for x in range(len(token)):
                if int(token[x])%2 ==0:
                    evenCount+=1
                else:
                    oddCount+=1
            if evenCount == len(token):
                return "even_numbers"
            elif oddCount == len(token):
                return "odd_numbers"
            else:
                return "random_numbers"
    else:
        if isSameCharacterSequence(token):
            return "same_sequence_specialchars"
        else:
            return "random_specialchars"

def tokeniser(tokenInfo):
    """
    Accepts a dictionary and maps the remaining parts of the source password.
    Goes through the reamining tokens and classifies them.
    Adds key - value pairs to the original dictionary under new classifications as defined in classifier.
    """

    source_pass = tokenInfo["source_pass"]
    tokensToSort = []
    tokensToClassify = []

    wordStartIndex = []
    wordEndIndex = []

    #Going through the words identified in the input and saving their start and end index in an array to use later
    if "words" not in tokenInfo["tokens"].keys():
        tokensToSort.append({
            "content": source_pass,
            "start_index": 0,
            "end_index": len(source_pass) - 1
            })

    else:
        for word in tokenInfo["tokens"]["words"]:
            wordStartIndex.append(word["start_index"])
            wordEndIndex.append(word["end_index"])

        tempTokenStartIndex = 0
        tempToken = ''
        for i in range(len(wordStartIndex)):
            tempToken = source_pass[tempTokenStartIndex:wordStartIndex[i]]
            if tempToken != '':
                tokensToSort.append({
                        "content": tempToken,
                        "start_index": tempTokenStartIndex,
                        "end_index": wordStartIndex[i] - 1
                    })
            tempTokenStartIndex = wordEndIndex[i] + 1

        if len(source_pass) > (wordEndIndex[len(wordEndIndex) - 1] + 1):
            tempToken = source_pass[wordEndIndex[len(wordEndIndex)-1]+1:len(source_pass)]
            tokensToSort.append({
                        "content": tempToken,
                        "start_index": wordEndIndex[len(wordEndIndex) - 1],
                        "end_index": len(source_pass) - 1
                    })

    for tokenBeingSorted in tokensToSort:
        if tokenBeingSorted["content"].isalpha() or tokenBeingSorted["content"].isdigit() or isOnlySpecialCharacters(tokenBeingSorted["content"]) or len(tokenBeingSorted["content"])==1:
            tokensToClassify.append({
                "content": tokenBeingSorted["content"],
                "start_index": tokenBeingSorted["start_index"],
                "end_index": tokenBeingSorted["end_index"]
            })
        else:
            tempTokenBeingSorted = tokenBeingSorted["content"][0]
            tempStartIndex = tokenBeingSorted["start_index"]

            for chars in range(len(tokenBeingSorted["content"]) -1):
                if classifyCharacter(tokenBeingSorted["content"][chars]) == classifyCharacter(tokenBeingSorted["content"][chars+1]):
                    tempTokenBeingSorted+=(tokenBeingSorted["content"][chars+1])
                else:
                    tokensToClassify.append({
                        "content": tempTokenBeingSorted,
                        "start_index": tempStartIndex,
                        "end_index": tempStartIndex + len(tempTokenBeingSorted) - 1
                    })
                    tempStartIndex += len(tempTokenBeingSorted)
                    tempTokenBeingSorted = tokenBeingSorted["content"][chars+1]

            tokensToClassify.append({
                "content": tempTokenBeingSorted,
                "start_index": tempStartIndex,
                "end_index": tempStartIndex + len(tempTokenBeingSorted) - 1
            })

    for token in tokensToClassify:

        unclassifiedToken = token["content"]
        classification = classifier(unclassifiedToken)
        if classification not in tokenInfo["tokens"]:
            tokenInfo["tokens"][classification] = []

        tokenInfo["tokens"][classification].append({
        "content": unclassifiedToken,
        "start_index": token["start_index"],
        "end_index": token["end_index"]
        })

    return tokenInfo