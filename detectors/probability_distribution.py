''' This version of program takes the RockYou passwords as input and parses them into sequence tokens.
It also calculates the probability of each token. It then reads sweetwords, parses them into sequence
tokens and calculates the probability for each sweetword.'''

probability_map = {}
total_tokens = 0

def define_probablities():
    rockyou_passwords = open("./resources/rockyou-frequent.txt").readlines()

    for password_line in rockyou_passwords:
        password_line = password_line.strip()
        datas = password_line.split()

        if len(datas) >= 2:
            record_occurance(datas[1], int(datas[0]))

    calculate_final_probability()
    print("probability_map final", probability_map)

def record_occurance(word, word_frequency):
    global total_tokens
    key_list =  []
    
    key_list = split_token_by_alpha_non_alpha(word)

    total_tokens = total_tokens + (word_frequency * len(key_list))

    for key in key_list:
        if key in probability_map:
            existing_probability = probability_map[key]

            new_probability = existing_probability + word_frequency
            probability_map[key] = new_probability
            
        else:
            new_probability = word_frequency
            probability_map[key] = new_probability

def calculate_final_probability():
    for key in iter(probability_map):
        existing_probability = probability_map[key]

        new_probability = round(float(existing_probability)/total_tokens, 5)
        probability_map[key] = new_probability
        

def get_most_probable_password(sweetwords):
    define_probablities()
    password_probability_map = {}
    
    for password in sweetwords:
        password_probability_map[password] = get_password_probability(password, probability_map)

    final_password_value = 0.0
    for key in iter(password_probability_map):
        value = password_probability_map[key]

        if final_password_value < value:
            final_password_value = value
            final_password = key

    return sweetwords.index(final_password)

def get_password_probability(password, probability_map):
    key_list =  []
    password_probability = 1.0

    key_list = split_token_by_alpha_non_alpha(password)
   
    for key in key_list:
        if key in probability_map:
            existing_probability = probability_map[key]
            password_probability = password_probability * existing_probability

    return round(password_probability, 5)
            
def split_token_by_alpha_non_alpha(token):
    originalSplitIndex = 0
    splitIndex = 0

    temp_token = token

    seq_tokens = []
    
    while splitIndex != -1:
        splitIndex = getSplitIndex(temp_token)
        
        if splitIndex == -1:
            seq_tokens.append(temp_token)
        else:
            seq_tokens.append(temp_token[:splitIndex])

            originalSplitIndex = originalSplitIndex + splitIndex
            temp_token = token[originalSplitIndex:]

            splitIndex = 0

    return seq_tokens

def getSplitIndex(token):    
    currentAlpha = 0
    previousAlpha = 0

    for i in range(len(token)):

        if i != 0:
            previousAlpha = currentAlpha

        currentChar = token[i]

        if currentChar.isalpha():
            currentAlpha = 1
        else:
            currentAlpha = 0

        if i != 0:
            if previousAlpha != currentAlpha:
                return i
    
    return -1


