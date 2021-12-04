"""
Make the commands that would run samples' vcf against their bed

input
    arg1: the path to all the coverage beds
    arg2+: The input VCF files

This tries to parse the names

Note - I don't feel like making this reusable by actually implementing the args
"""
import os
import sys
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
        
prog="python3 scripts/pvcf_hc_region_annotate.py"
for fh in sys.argv[1:]:
    #data/short_read_calls/genotyping/biograph/NA19239/chm13.results.vcf.gz
    data = fh.split('/')
    samp = data[-2]
    ref = data[-1].split('.')[0]
    out_name = fh[:-len(".vcf.gz")] + '.covanno.vcf.gz'
    found = []
    for i in bed_lookup[ref]:
        if samp in i:
            found.append(i)
    found.sort()
    print(f"{prog} {fh} {found[0]} {found[1]} | bgzip > {out_name}")
        
