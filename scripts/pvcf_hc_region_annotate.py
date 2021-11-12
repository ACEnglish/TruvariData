"""
This only works for intra sample single VCF and the pair of beds
"""
import sys
import pysam
import truvari
from intervaltree import IntervalTree
from collections import defaultdict

vcf_fn = sys.argv[1]
mat_bed_fn = sys.argv[2]
pat_bed_fn = sys.argv[3]

def bed_to_tree(bed_fn):
    lookup = defaultdict(IntervalTree)
    with open(bed_fn, 'r') as fh:
        for line in fh:
            chrom, start, end, cov = line.strip().split('\t')
            start = int(start)
            end = int(end)
            cov = int(cov)
            lookup[chrom].addi(start, end, data=cov)
    return lookup

pat_lookup = bed_to_tree(pat_bed_fn)
mat_lookup = bed_to_tree(mat_bed_fn)

vcf = pysam.VariantFile(vcf_fn)
n_header = vcf.header.copy()
n_header.add_line(('##FORMAT=<ID=DIPCOV,Number=1,Type=Integer,'
                   'Description="Singly covered by each haplotype (bool: 0, 1)"'))
out = pysam.VariantFile("/dev/stdout", 'w', header=n_header)

for entry in vcf:
    #sz = truvari.entry_size(entry)
    #if sz >= 50:
    #    continue
    entry = truvari.copy_entry(entry, n_header)
    up_pos = list(mat_lookup[entry.chrom].at(entry.start))[0].data
    dn_pos = list(mat_lookup[entry.chrom].at(entry.stop))[0].data
    #entry.info["A1COV"] = [up_pos, dn_pos]
    is_dip = up_pos == 1 and dn_pos == 1
    up_pos = list(pat_lookup[entry.chrom].at(entry.start))[0].data
    dn_pos = list(pat_lookup[entry.chrom].at(entry.stop))[0].data
    #entry.info["A2COV"] = [up_pos, dn_pos]
    is_dip = is_dip and up_pos == 1 and dn_pos == 1
    entry.samples[0]["DIPCOV"] = int(is_dip)

    out.write(entry)
        

