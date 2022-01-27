import glob
import pandas as pd
import json
import joblib

fns = glob.glob("temp/*/summary.txt")
gt_map = {'(1, 1)': "HOM", '(1, 0)': 'HET', '(0, 1)': 'HET'}
parts = []
for i in fns:
    ref, pvcf, caller, sample = i.split('/')[-2].split('_')
    d = json.load(open(i))
    x = pd.DataFrame(d['gt_matrix'])
    c = x.columns.map(gt_map)
    x.columns = c
    x.set_index(x.index.map(gt_map), inplace=True)
    del(d['gt_matrix'])
    d['gt_concordance'] = (x.loc["HET"]["HET"].sum().sum() + x.loc['HOM']['HOM']) / x.sum().sum()
    d['reference'] = ref
    d['pVCF merge'] = pvcf
    d['caller'] = caller
    d['sample'] = sample
    parts.append(d)

parts = pd.DataFrame(parts)
parts['pVCF merge'] = parts['pVCF merge'].map({'truvari':"Truvari", 
                                     "survivor":"SURVIVOR", 
                                     "naive":"Naive", 
                                     "jasmine":"Jasmine",
                                    "exact":"BCFtools"})
parts.to_csv('bench_summary.txt', index=False, sep='\t')
