import os
import sys
import glob
import joblib
import pandas as pd

all_data = []
out_name = sys.argv[1]
in_files = sys.argv[2:]
for i in in_files:
    all_data.append(joblib.load(i))
out = pd.concat(all_data)
out = out[out["VARLEN"] >= 50]
joblib.dump(out, out_name)
