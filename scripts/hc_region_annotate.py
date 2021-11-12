import sys
import pysam
import truvari
from intervaltree import IntervalTree
from collections import defaultdict

vcf_fn = sys.argv[1]
bed_fn = sys.argv[2]

lookup = defaultdict(IntervalTree)
with open(bed_fn, 'r') as fh:
    for line in fh:
        chrom, start, end, cov = line.strip().split('\t')
        start = int(start)
        end = int(end)
        cov = int(cov)
        lookup[chrom].addi(start, end, data=cov)

vcf = pysam.VariantFile(vcf_fn)
n_header = vcf.header.copy()
n_header.add_line(('##INFO=<ID=ASMCOV,Number=.,Type=Integer,'
                   'Description="Coverage of Assemblies of start/end breakpoints">'))
n_header.add_line(('##INFO=<ID=DIPCOV,Number=0,Type=Flag,'
                   'Description="Singly covered by each haplotype across all samples"'))

out = pysam.VariantFile("/dev/stdout", 'w', header=n_header)
hap_cnt = len(vcf.header.samples) * 2
for entry in vcf:
    #sz = truvari.entry_size(entry)
    #if sz < 50:
    #    continue
    entry = truvari.copy_entry(entry, n_header)
    up_pos = list(lookup[entry.chrom].at(entry.start))[0].data
    dn_pos = list(lookup[entry.chrom].at(entry.stop))[0].data
    entry.info["ASMCOV"] = [up_pos, dn_pos]
    is_dup = up_pos == hap_cnt and dn_pos == hap_cnt 
    entry.info["DIPCOV"] = is_dup
    out.write(entry)
        

