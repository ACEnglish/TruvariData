import glob
import truvari
import pandas as pd

meta = pd.read_csv("../../metadata/sample_metadata.txt", sep='\t')
# Make a ped
rows = []
for fam, i in meta.groupby(["FamilyId"]):
    if fam in ['RM8392', "RM8393", "RM8398"]: continue
    if len(i) != 3: continue
    f = i[i["TrioState"] == 'father']['Individual'].iloc[0]
    m = i[i["TrioState"] == 'mother']['Individual'].iloc[0]
    c = i[i["TrioState"] == 'child']['Individual'].iloc[0]
    rows.append([m, f, c])
ped = pd.DataFrame(rows)
ped.to_csv('fams.ped', header=False, index=False)

def parse_results(stdout, ref, method, which):
    rows = []
    for line in stdout.split('\n'):
        if line.startswith("#"): continue
        if line == "": continue
        l = line.strip().split('\t')
        l.append(ref)
        l.append(method)
        l.append(which)
        rows.append(l)
    return rows

results = []
for vcf in glob.glob("data/*/*.vcf.gz"):
    #If you want the 'best covered' sites
    #ret = truvari.cmd_exe(f"bcftools view -i 'ASMCOV[0] == 72' {vcf} | bcftools +mendelian -c --trio-file fams.ped")
    ret = truvari.cmd_exe(f"bcftools +mendelian -c --trio-file fams.ped {vcf}")
    ref = vcf.split('/')[-2]
    method = vcf.split('/')[-1].split('.')[0]
    data = parse_results(ret.stdout, ref, method, 'all')
    results.extend(data)
    for pos, d in ped.iterrows():
        d = ",".join(list(d))
        ret = truvari.cmd_exe(f"bcftools view -s {d} {vcf} | vcf-subset -e | bcftools +mendelian -c --trio {d}")
        data = parse_results(ret.stdout, ref, method, 'present')
        results.extend(data)
        

results = pd.DataFrame(results, columns=["nOk", "nBad", "nSkipped", "Trio", "Reference", "Merge", "Variants"])
results.to_csv('mendelian_raw.txt', sep='\t', index=False)
results['nOk'] = results['nOk'].astype(int)
results['nBad'] = results['nBad'].astype(int)
results['nSkipped'] = results['nSkipped'].astype(int)
results['MendErr'] = results['nBad'] / (results['nBad'] + results['nOk'])

results.to_csv('mendelian.txt', sep='\t', index=False)
