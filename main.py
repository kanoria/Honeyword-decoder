import argparse
from detectors.entropy import detect_password as entropy_detector
from detectors.markov import detect_outlier as markov_detector
from detectors.similarity import get_dissimilar_password as similarity_detector

parser = argparse.ArgumentParser(description='Detect passwords in honey list')

parser.add_argument('n', type=int)
parser.add_argument('m', type=int) # we assume that all the password are on one
#  line so we don't need that one parameter
parser.add_argument('input_passwords_file', type=file)

args = parser.parse_args()

to_be_inspected = []
index = 0

for line in args.input_passwords_file:
    if len(to_be_inspected) < (index + 1):
        to_be_inspected.append(map(lambda w: w.strip(), line.split(",")))
    elif len(to_be_inspected[index]) < args.n:
        to_be_inspected[index] += map(lambda w: w.strip(), line.split(","))

    if len(to_be_inspected[index]) == args.n:
        index += 1

detection_algorithms = [
    {
        "fct": entropy_detector,
        "weight": 0.5
    },{
        "fct": markov_detector,
        "weight": 1
    }, {
        "fct": similarity_detector,
        "weight": 2
    }
]


def detect_real_password(password_list):

    scores = [0 for x in range(len(password_list))]

    for algorithm in detection_algorithms:
        idx = algorithm["fct"](password_list)
        if idx != -1:
            scores[idx] += algorithm["weight"]

    print scores
    return scores.index(max(scores))


indexes = map(detect_real_password, to_be_inspected)
print indexes
for index in xrange(len(to_be_inspected)):
    print to_be_inspected[index][indexes[index]]
