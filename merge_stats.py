import sys
import joblib
import pandas as pd
import glob

pd.set_option("display.max_rows", None)
all_vars = []
for i in sys.argv[1:]:
    d = joblib.load(i)
    col_name = i[:-len(".vcf.gz.jl")]
    d[col_name] = 1
    view = d.groupby(["svtype", "szbin"]).sum().loc[["DEL", "INS"], col_name]
    all_vars.append(view)

all_vars = pd.concat(all_vars, axis=1)
print(all_vars)
joblib.dump(all_vars, "asm_stats.jl")
