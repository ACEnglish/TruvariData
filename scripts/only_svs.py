import sys
import pysam
import truvari

v = pysam.VariantFile(sys.argv[1])
passonly = False
if len(sys.argv) == 3:
    passonly = True
o = pysam.VariantFile("/dev/stdout", 'w', header=v.header)
for entry in v:
    if passonly and truvari.entry_is_filtered(entry):
        continue
    if abs(len(entry.alts[0]) - len(entry.ref)) >= 50:
        o.write(entry)
