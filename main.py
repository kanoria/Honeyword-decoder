import argparse
import detectors.entropy

parser = argparse.ArgumentParser(description='Detect passwords in honey list')

parser.add_argument('n', type=int)
parser.add_argument('m', type=int)
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

indexes = map(detectors.entropy.detect_password, to_be_inspected)
print indexes
for index in xrange(len(to_be_inspected)):
    print to_be_inspected[index][indexes[index]]

