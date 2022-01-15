import glob
import json
import joblib
import pandas as pd

files = glob.glob("*bench/*/summary.txt")
rows = []
for f in files:
    prog = f.split('_')[0]
    ref, sample = f.split('/')[1].split('_')
    data = json.load(open(f))
    del(data["gt_matrix"])
    x = pd.Series(data)
    x["merge"] = prog
    x["reference"] = ref
    x["sample"] = sample
    rows.append(x)
out = pd.concat(rows, axis=1).T
joblib.dump(out, "benchsummary.jl")
print(out)
