"""
Separate the exact calls by their haplotype
"""
import sys
import pysam

in_vcf = pysam.VariantFile(sys.argv[1])
out1_vcf = pysam.VariantFile(sys.argv[2] + "_h1.vcf", 'w', header=in_vcf.header)
out2_vcf = pysam.VariantFile(sys.argv[2] + "_h2.vcf", 'w', header=in_vcf.header)

for entry in in_vcf:
    if abs(len(entry.alts[0]) - len(entry.ref)) >= 50:
        if entry.samples[0]["GT"][0] == 1:
            out1_vcf.write(entry)
        if entry.samples[0]["GT"][1] == 1:
            out2_vcf.write(entry)
