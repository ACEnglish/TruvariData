import glob
import pandas as pd

ref_paths = {'grch38': "/users/u233287/scratch/insertion_ref/msru/data/reference/grch38/GRCh38_1kg_mainchrs.fa",
             'chm13': "/users/u233287/scratch/insertion_ref/msru/data/reference/chm13/chm13.draft_v1.0.fasta",
             'hg19': "/users/u233287/scratch/insertion_ref/msru/data/reference/hg19/hg19.fa"}

calls = glob.glob("data/discovery/manta/*.vcf.gz")
calls.extend(glob.glob("data/discovery/biograph/*.vcf.gz"))

pvcfs = glob.glob("../inter_sample_merge/data/*/*.vcf.gz")
rows = []
for i in pvcfs:
    data = i.split('/')
    ref = data[3]
    prog = data[4].split('.')[0]
    rows.append([ref, prog, i])
pvcfs = pd.DataFrame(rows, columns=["ref", "merge", "path"])
merges = pvcfs["merge"].unique()
pvcfs.set_index(['ref', 'merge'], inplace=True)

rows = []
for i in calls:
    data = i.split('/')
    prog = data[2]
    x = data[3].split('.')
    sample = x[0]
    ref = "grch38" if x[1] == 'sv' else x[1]
    rows.append([ref, prog, sample, i])
    
calls = pd.DataFrame(rows, columns=["ref", "prog", "sample", "path"])

name = 0
for i, c in calls.iterrows():
    for m in merges:
        ref = c["ref"]
        if ref != 'chm13' or m != 'jasmine':
            continue
        ref_fn = ref_paths[ref]

        base = pvcfs.loc[ref, m]['path']
        prog = c["prog"]
        comp = c["path"]
        samp = c['sample']
        out_name = f"temp/{ref}_{m}_{prog}_{samp}"
        with open(f'jobs/bench_{name}.sh', 'w') as fout:
            fout.write(f"truvari bench -b {base} -c {comp} -f {ref_fn} -o {out_name} --bSample {samp} --no-ref b")
        name += 1
