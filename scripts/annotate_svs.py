import sys
import pysam
import truvari

v = pysam.VariantFile(sys.argv[1])
header = v.header.copy()
header.add_line(('##INFO=<ID=SVTYPE,Number=1,Type=String,'
                     'Description="SV type">'))
header.add_line(('##INFO=<ID=SVLEN,Number=1,Type=Integer,'
                     'Description="SV length">'))
o = pysam.VariantFile("/dev/stdout", 'w', header=header)
for entry in v:
    sz = len(entry.alts[0]) - len(entry.ref)
    if abs(sz) >= 25:
        entry.translate(header)
        if sz < 0:
            entry.info["SVTYPE"] = "DEL"
        else:
            entry.info["SVTYPE"] = "INS"
        entry.info["SVLEN"] = sz
    o.write(entry)

