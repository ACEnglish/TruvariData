import sys
import joblib
import pandas as pd


base = joblib.load(sys.argv[1])
comp = joblib.load(sys.argv[2])
out_name = sys.argv[3]

samples = [_.split('_')[0] for _ in base.columns if _.endswith("_GT") and _ in comp.columns]
data = base.join(comp, rsuffix='_')
for samp in samples:
    data[samp] = data[samp + "_GT"] == data[samp + "_GT" + "_"]
#defragment
data = data.copy()
joblib.dump(data, out_name)
