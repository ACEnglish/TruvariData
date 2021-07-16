import os
import sys
import glob
from pathlib import Path

import joblib
import truvari
import pandas as pd

from pandas.api.types import CategoricalDtype
SZBINTY = CategoricalDtype(categories=truvari.SZBINS[1:], ordered=True)

all_data = []
for jl in Path(sys.argv[1]).rglob("*.jl"):
    split_path = str(jl).split('/')
    d = joblib.load(jl)
    d.reset_index(inplace=True)
    d.drop(columns=['key', 'id', 'qual', 'filter', 'is_pass'], inplace=True)
    d["GT"] = d["GT"].apply(lambda x: truvari.get_gt(x).name)
    ref, proj, samp, merge = split_path[-4:]
    merge = merge[:-len(".jl")]
    d[["reference", "project", "sample", "merge"]] = ref, proj, samp, merge
    all_data.append(d)

out = pd.concat(all_data)
out["szbin"] = out["szbin"].astype(SZBINTY)
joblib.dump(out, sys.argv[2])
