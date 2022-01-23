import sys
import truvari
import pandas as pd

sv_count = []
af_dist = []
sz_dist = []

for fn in sys.argv[1:]:
    name = fn.split('/')
    reference = name[1]
    merge = name[2].split('.')[0]
    df = truvari.vcf_to_df(fn, with_info=True)

    # SVCounts by Type/Merge/reference
    sv = df.groupby(['svtype']).size().to_frame('count').reset_index()
    sv['reference'] = reference
    sv['merge'] = merge
    sv_count.append(sv)

    # AFs by Merge/reference
    df['AF'] = df['AF'].apply(lambda x: x[0])
    af = df.groupby(['svtype'])["AF"].mean().reset_index()
    af['reference'] = reference
    af['merge'] = merge
    af_dist.append(af)

    # SizeDistribution by Merge/reference
    sz = df.groupby(['svtype', 'szbin']).size().to_frame('count').reset_index()
    sz['reference'] = reference
    sz['merge'] = merge
    sz_dist.append(sz)

sv_count = pd.concat(sv_count)
sv_count.to_csv("all_svty_count.txt", sep='\t', index=False)

af_dist = pd.concat(af_dist)
af_dist.to_csv("all_af_dist.txt", sep='\t', index=False)

sz_dist = pd.concat(sz_dist)
sz_dist.to_csv("all_sz_dist.txt", sep='\t', index=False)
