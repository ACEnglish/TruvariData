import sys
import truvari
import pandas as pd
import pysam
sv_count = []

for fn in sys.argv[1:]:
    name = fn.split('/')
    reference = name[1]
    merge = name[2].split('.')[0]
    cnt = 0
    v = pysam.VariantFile(fn)
    for entry in v:
        cnt += 1
    sv_count.append([reference, merge, cnt])

sv_count = pd.DataFrame(sv_count, columns=["Reference", "Merge", "Count"])
sv_count.to_csv("pvcf_count.txt", sep='\t', index=False)
