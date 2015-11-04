import os.path
from tqdm import *


ROCK_YOU_DB = "./resources/rockyou-withcount.txt"
MARKOV_FILE = "./resources/duet.txt"


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

        if len(data) > 1:
            for char in data[1]:
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
        f.write(duet + " " + str(duet_dict[duet]) + "\n")
    f.close()


def load_duet():
    """ Loads the markov file from the disk into memory
    :return: dictionary with duet as keys and probabilities as values
    """
    duet = {}

    f = open(MARKOV_FILE, 'r')
    for line in f:
        data = line.strip().split(" ")
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


get_duet_probabilities()