import editdistance

def rankSyntacticSimilarity(honeywords):
    dict = collections.OrderedDict()
    for honeyword in honeywords:
        sum = 0.0;
        for honeyword2 in honeywords:
            if(honeyword != honeyword2):
             sum += editdistance.eval(honeyword,honeyword2)
        sum = sum/(len(honeywords)-1)
        if(not dict.has_key(sum)):
            dict[sum] = [];
        dict[sum].append(honeyword)
    return dict