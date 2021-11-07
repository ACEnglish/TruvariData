"""
This only works for inter sample because we just the the total allele coverage of all the single_coverage regions.
For a intra-merge, I need to provide a haplotype for each
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
n_header.add_line(('##INFO=<ID=A1COV,Number=.,Type=Integer,'
                   'Description="Coverage of First Assembly of start/end breakpoints">'))
n_header.add_line(('##INFO=<ID=A2COV,Number=.,Type=Integer,'
                   'Description="Coverage of Second Assembly of start/end breakpoints">'))
n_header.add_line(('##INFO=<ID=DIPCOV,Number=0,Type=Flag,'
                   'Description="Singly covered by each haplotype"'))
out = pysam.VariantFile("/dev/stdout", 'w', header=n_header)

for entry in vcf:
    sz = truvari.entry_size(entry)
    #if sz >= 50:
    #    continue
    entry = truvari.copy_entry(entry, n_header)
    up_pos = list(mat_lookup[entry.chrom].at(entry.start))[0].data
    dn_pos = list(mat_lookup[entry.chrom].at(entry.stop))[0].data
    entry.info["A1COV"] = [up_pos, dn_pos]
    is_dip = up_pos == 1 and dn_pos == 1
    up_pos = list(pat_lookup[entry.chrom].at(entry.start))[0].data
    dn_pos = list(pat_lookup[entry.chrom].at(entry.stop))[0].data
    entry.info["A2COV"] = [up_pos, dn_pos]
    is_dip = is_dip and up_pos == 1 and dn_pos == 1
    entry.info["DIPCOV"] = is_dip

    out.write(entry)
        

