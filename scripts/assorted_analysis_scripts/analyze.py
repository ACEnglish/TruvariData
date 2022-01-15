
"""
For each sample, 

Matrix of BaseGt by CompGt

Do it again for each SVTYPE...?

I wonder if I can make a N-dimensional array..

But I'm also interested in NumNeighbors...

Maybe I should just take out the minimal information. encode the genotypes. and take the states
and the svtype, szbin, 

AF, MAF, svtype, szbin, REMAP, NumCollapsed, TRF, TRFperiod, TRFcopies NumNeighbors, ASMCOV


Fuck, do I need the DP / FT?
"""
import sys
import joblib
import numpy as np
import pandas as pd
import truvari

samples = ["HG00096", "HG00171", "HG00512", "HG00513", "HG00514", "HG00731",
"HG00732", "HG00733", "HG00864", "HG01114", "HG01505", "HG01596", "HG02011", "HG02492", "HG02587",
"HG02818", "HG03009", "HG03065", "HG03125", "HG03371", "HG03486", "HG03683", "HG03732", "NA12329",
"NA18534", "NA18939", "NA19238", "NA19239", "NA19240", "NA19650", "NA19983", "NA20509", "NA20847"]

def make_numbers(data):
    ret = []
    for sample in data:
        x = data[sample]
        correct = x["HET"]["HET"] + x["HOM"]["HOM"] + x["REF"]["REF"]
        total = x.sum().sum()
        concordance = correct / total
        p_correct = x.loc[["HET", "HOM"], ["HET", "HOM"]].sum().sum() + x.loc["REF", "REF"]
        presence = p_correct / total

        ret.append([sample, concordance, presence])
    return ret

def make_matrix(df, samples):
    """
    """
    ret = {}
    for i in samples:
        base_col = i + "_GT"
        comp_col = i + "_GT_"
        a = df[base_col].apply(lambda x: truvari.get_gt(x).name if isinstance(x, tuple) else 'UNK')
        b = df[comp_col].apply(lambda x: truvari.get_gt(x).name if isinstance(x, tuple) else 'UNK')
        j = pd.concat([a, b], axis=1)
        view = j.value_counts().unstack()
        ret[i] = view
    return make_numbers(ret)


in_fn, out_fn = sys.argv[1:]
data = joblib.load(in_fn)
keep = ~data.index.str.startswith("chrY") & ~data.index.str.startswith("chrX")
data = data[keep]

for i in samples:
    # Setting the Genotypes to the easier set
    data[i + "_GT"] = data[i +  "GT"].apply(lambda x: truvari.get_gt(x).name if isinstance(x, tuple) else 'UNK')
    data[i + "_GT_"] = data[i +  "GT"].apply(lambda x: truvari.get_gt(x).name if isinstance(x, tuple) else 'UNK')

output = {}
output["overall"] = make_matrix(data, samples)

view = data["svtype"] == "DEL"

cur = make_matrix(data, i + "_GT", i + "_GT_")

# Filter the variants here
joblib.dump(parts, out_fn)


# Do it by SVTYPE
# Do it by FT == PASS (if it's a thing)
# Do it by NumNeighbors (because I know that's a thing)
# Anything about sizebin
