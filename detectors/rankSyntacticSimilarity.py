import editdistance
import collections
import numpy
import random


# Computes how 'sparse' the honeywords are. If the honeywords are syntactically close to each other
# it attemps to find the root word out of which all other honeywords were generated.
# we set the thresh-hold to a maximum of 55% average changes from a root word to decide whether the
# list is sparse or not.


def rankSyntaticSimilarityOfHoneyWords(honeywords):
    dict = {}

    #compute the average edit distance of each word to everybody else
    for honeyword in honeywords:
        sum =0.0;
        for honeyword2 in honeywords:
            if(honeyword != honeyword2): #normalize the average edit distance to the max edit distance
             sum+=float(editdistance.eval(honeyword,honeyword2))/max(len(honeyword),len(honeyword2))
        sum = sum/(len(honeywords)-1)
        if(not dict.has_key(sum)):
            dict[sum] = [];
        dict[sum].append(honeyword)

    #print numpy.array(dict.keys()).std()*100
    #print numpy.array(dict.keys()).mean()*100
    minPercentChange = min(dict.keys())

    #print dict[minPercentChange]
    if(minPercentChange < 0.55):
        return honeywords.index(dict[minPercentChange][random.randint(0, len(dict[minPercentChange])-1)])
    return -1