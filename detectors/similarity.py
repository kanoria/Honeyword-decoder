import editdistance
import random


def get_dissimilar_password(honeywords):
    """
     Computes how 'sparse' the honeywords are. If the honeywords are
     syntactically close to each other it attemps to find the root word out of
     which all other honeywords were generated.we set the thresh-hold to a
     maximum of 55% average changes from a root word to decide whether the list
     is sparse or not.

     :param honeywords: list of honeywords from which the real password has to
                        be found
     :return: index of the password found or -1 if nothing is found
     """

    mapper = {}

    # compute the average edit distance of each word to everybody else
    for honeyword in honeywords:
        acc = 0.0
        for honeyword2 in honeywords:
            # normalize the average edit distance to the max edit distance
            if honeyword != honeyword2:
                acc += float(editdistance.eval(honeyword, honeyword2))/max(
                    len(honeyword), len(honeyword2))

        acc /= (len(honeywords)-1)

        if acc not in mapper:
            mapper[acc] = []

        mapper[acc].append(honeyword)

    min_percent_change = min(mapper.keys())

    # print dict[minPercentChange]

    if min_percent_change >= 0.55:
        return -1

    return honeywords.index(mapper[min_percent_change]
                            [random.randint(0,
                                            len(mapper[min_percent_change])-1)])
