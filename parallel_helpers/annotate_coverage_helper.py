"""
Make the commands that would run samples' vcf against their bed

input
    arg1: the path to all the coverage beds
    arg2+: The input VCF files

This tries to parse the names

Note - I don't feel like making this reusable by actually implementing the args
"""
import os
import glob
from collections import defaultdict

bed_files = glob.glob("data/coverage_beds/*.bed")
bed_lookup = defaultdict(list)
for line in bed_files:
    name = os.path.basename(line)
    if name.startswith("GRCh38"):
        bed_lookup['grch38'].append(line)
    elif name.startswith("chm13"):
        bed_lookup['chm13'].append(line)
    elif name.startswith("hg19"):
        bed_lookup['hg19'].append(line)
        
prog="python3 scripts/intra_hc_region_annotate.py"
with open("temp/covanno.tasks.txt") as fh:
    for line in fh:
        line = line.strip()
        data = line.split('/')
        ref = data[2]
        samp = data[4]
        out_name = line[:-len(".vcf.gz")] + '.covanno.vcf.gz'
        found = []
        for i in bed_lookup[ref]:
            if samp in i:
                found.append(i)
        found.sort()
        print(f"{prog} {line} {found[0]} {found[1]} | bgzip > {out_name}")
        
