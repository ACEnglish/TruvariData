import sys
import pysam

v = pysam.VariantFile(sys.argv[1])
o = pysam.VariantFile("/dev/stdout", 'w', header=v.header)
for entry in v:
    if abs(len(entry.alts[0]) - len(entry.ref)) >= 50:
        o.write(entry)
