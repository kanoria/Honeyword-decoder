import os.path
import math
from tqdm import *


ROCK_YOU_DB = "./resources/rockyou-withcount.txt"
MARKOV_FILE = "./resources/duet.txt"


# Heavily inspired by markov chains

def generate_duet_prob():
    """ Generates a dictionary with the probability of each duet
    :return: duet as key and probability as value
    """

    print "Generating duet probabilities ..."

    if not os.path.isfile(ROCK_YOU_DB):
        print "In order to generate the duet probabilities, we need the \n" \
              "rockyou-withcount.txt file. Please put it in the resources \n" \
              "folder and run the program again."
        return -1

    rock_you = open(ROCK_YOU_DB, 'r')
    temp = ""
    duet_probability = {}

    # number of total duets
    total_count = 0.0

    for line in tqdm(rock_you):
        data = line.strip().split(" ")

        if len(data) > 2:
            password = " ".join(data[1:])
        elif len(data) > 1:
            password = data[1]
        else:
            password = ""

        for char in password:
            if temp == "":
                temp = char
            else:
                duet = temp + char
                if duet in duet_probability:
                    duet_probability[duet] += float(data[0])
                else:
                    duet_probability[duet] = float(data[0])
                total_count += float(data[0])

        temp = ""
    rock_you.close()

    for duet in duet_probability.keys():
        duet_probability[duet] = duet_probability[duet] / total_count

    print "--> done"

    return duet_probability


def save_duet(duet_dict):
    """ Save the markov data structure in a file
    :param duet_dict: markov data structure
    :return: void
    """
    f = open(MARKOV_FILE, 'w+')
    for duet in duet_dict.keys():
        f.write(duet + "separator" + str(duet_dict[duet]) + "\n")
    f.close()


def load_duet():
    """ Loads the markov file from the disk into memory
    :return: dictionary with duet as keys and probabilities as values
    """
    duet = {}

    f = open(MARKOV_FILE, 'r')
    for line in f:
        data = line.strip().split("separator")
        # print line
        # print data
        duet[data[0]] = float(data[1])
    f.close()

    return duet


def get_duet_probabilities():
    """ get the duet probabilities from the rock you database.
    :return: a dictionary with the duet as value
    """
    if not os.path.isfile(MARKOV_FILE):
        duet = generate_duet_prob()
        save_duet(duet)
        return duet
    else:
        return load_duet()


def detect_outlier(password_list):
    """ Computes the maximum log likelyhood of having a password modeling as
    a markov chain. As a consequence, the password is a represented as a
    sequence of letters on which is probability only depends on the probability
    of the sequence with the previous letter. As a consequence, we can
    compute the log likelihood as the sum of the logs of the probabilities
    of the letter duet sequences.

    :param password_list: list of password to get the
    :return: index of the password detected as the real password, -1 if nothing
    was found
    """

    duets = get_duet_probabilities()

    def compute_likelihood(password):
        """ Computes the likelihood of the password having that sequence of
        characters according to the rock you database and the markov model

        :param password: password being tested
        :return: the log likelihood of the password.
        """

        if len(password) == 0:
            return -1

        temp = ""
        likelihood = 0
        for char in password:
            if temp == "":
                temp = char
            else:
                duet = temp + char
                if duet in duets:
                    likelihood += math.log(duets[duet])

        return likelihood

    scores = map(compute_likelihood, password_list)
    return scores.index(max(scores))
