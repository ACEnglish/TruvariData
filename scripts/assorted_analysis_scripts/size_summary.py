import sys
import truvari
import pandas as pd

out_name = sys.argv[1]
in_names = sys.argv[2:]

for fn in in_names:
    data = truvari.vcf_to_df(fn, with_info=True)
    view = data.groupby(['svtype', 'szbin']).size().reset_index()
    view['file'] = fn
    parts.append(view)
