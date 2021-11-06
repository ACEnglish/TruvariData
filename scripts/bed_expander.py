import sys

BUFFER=10000
lookup = {}
with open(sys.argv[1], 'r') as fh:
    for line in fh:
        data = line.strip().split('\t')
        lookup[data[0]] = int(data[1])

for line in sys.stdin:
    data = line.strip().split('\t')
    data[1] = int(data[1])
    data[2] = int(data[2])
    data[1] = str(max(0, data[1] - BUFFER))
    data[2] = str(min(lookup[data[0]], data[2] + BUFFER))
    print("\t".join(data))
