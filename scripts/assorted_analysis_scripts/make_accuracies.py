import sys
import joblib


data = joblib.load(sys.argv[1])
print('sample concordance presence')
for sample in data:
    x = data[sample]
    correct = x["HET"]["HET"] + x["HOM"]["HOM"] + x["REF"]["REF"]
    total = x.sum().sum()
    concordance = correct / total
    p_correct = x.loc[["HET", "HOM"], ["HET", "HOM"]].sum().sum() + x.loc["REF", "REF"]
    presence = p_correct / total

    print(sample, concordance, presence)
