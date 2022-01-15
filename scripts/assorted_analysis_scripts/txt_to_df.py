import sys
import pandas
import hashlib


def load_txt(fn):
    d = pandas.read_csv(sys.argv[1], sep="\t", header=None)
    d.columns = ["CHROM", "POS", "NeighId", "SVLEN", "SVTYPE",
                 "TRFcopies", "TRFDiff", "TRFrepeat", "ALT"]
    def mk_key(line):
        result = hashlib.md5(f"{line['CHROM']} {line['POS']} {line['ALT']} {line['SVTYPE']}".encode())
        return result.hexdigest()

    d = d[(d["SVTYPE"] == 'INS') & (d["TRFDiff"] != ".")]
    d["var key"] = d.apply(mk_key, axis=1)
    d["TRFDiff"] = d["TRFDiff"].astype(float)
    return d

exact = 
for mid, dat in d.groupby(["NeighId", "TRFrepeat"]):
    j = dat["TRFDiff"].value_counts()
    print(mid)
    print(dat["TRFDiff"].value_counts())
    break
    # drop na from TRFDiff... 
    # I'm trying
