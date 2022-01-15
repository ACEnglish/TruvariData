import sys
import joblib
import pandas as pd

parts = []
for i in sys.argv[1:]:
    d = pd.read_csv(i)
    merge, ref = i.split('.')[:2]
    d['merge'] = merge
    d['ref'] = ref
    parts.append(d)
d = pd.concat(parts)
joblib.dump(d, 'size_summary.jl')
