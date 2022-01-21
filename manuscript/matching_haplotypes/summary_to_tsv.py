import sys
import json

data = json.load(open(sys.argv[1], 'r'))

for i in ["TP-base", "TP-call", "FP", "FN", "precision", "recall", "f1", "base cnt", "call cnt", "gt_concordance"]:
    sys.stdout.write(str(data[i]) + '\t')
sys.stdout.write('\n')
