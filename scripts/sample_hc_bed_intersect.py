import sys
import pysam
import truvari
from collections import defaultdict
from intervaltree import IntervalTree

def bed_to_tree(in_file):
    lookup = defaultdict(IntervalTree)
    with open(in_file, 'r') as fh:
        for line in fh:
            chrom, start, end, cov = line.strip().split('\t')
            start = int(start)
            end = int(end)
            cov = int(cov)
            lookup[chrom].addi(start, end, data=cov)
    return lookup

def main():
    sample = sys.argv[1]
    vcf_fn = sys.argv[2]
    h1_bed = sys.argv[3]
    h2_bed = sys.argv[4]
    h1 = bed_to_tree(h1_bed)
    h2 = bed_to_tree(h2_bed)
    vcf = pysam.VariantFile(vcf_fn)
    rows = []
    for entry in vcf:
        if entry.samples[sample]["GT"] == (0, 0):
            continue
        sz = truvari.entry_size(entry)
        if sz < 50:
            continue
        ty = truvari.entry_variant_type(entry)
        cov1_s = list(h1[entry.chrom].at(entry.start))[0].data
        cov1_e = list(h1[entry.chrom].at(entry.stop))[0].data
        cov2_s = list(h2[entry.chrom].at(entry.start))[0].data
        cov2_e = list(h2[entry.chrom].at(entry.stop))[0].data
        g1, g2 = entry.samples[sample]["GT"]
        print(sz, ty, f"{g1}_{g2}", cov1_s, cov1_e, cov2_s, cov2_e)

if __name__ == '__main__':
    main()
