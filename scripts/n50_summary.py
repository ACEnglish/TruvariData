"""
Reformats n50 stats output into a dataframe
Provide a tsv (with header) and columns of 
project sample_name  hap fn
"""
import sys
import pandas as pd
import joblib
from collections import OrderedDict

def reformat(fn):
    data = OrderedDict()
    intstrip = lambda line: int(line.strip().split('\t')[1])
    with open(fn) as fh:
        for line in fh:
            if line.startswith("CC"):
                continue
            if line.startswith("GS"):
                data["gs"] = intstrip(line)
            elif line.startswith("SZ"):
                data["sz"] = intstrip(line)
            elif line.startswith("NN"):
                data["nn"] = intstrip(line)
            elif line.startswith("NL"):
                line = line.strip().split('\t')
                data[f"n50_{line[1]}_len"] = int(line[2])
                data[f"n50_{line[1]}_cnt"] = int(line[3])
            elif line.startswith("AU"):
                data["au"] = intstrip(line)
            else:
                print(f"error in {fn}: {line}")
                exit(1)

    return pd.DataFrame([data])

def main():
    all_data = []
    in_file, out_jl = sys.argv[1:]
    with open(in_file, 'r') as fh:
        for line in fh:
            project, samp, hap, fn = line.strip().split('\t')
            data = reformat(fn)
            data["project"] = project
            data["sample"] = samp
            data["hap"] = hap
            all_data.append(data)

    data = pd.concat(all_data)
    joblib.dump(data, out_jl)

def test():
    fn = "/users/u233287/scratch/insertion_ref/long_read_data/stats/v12_NA19983_hgsvc_pbsq2-clr_1000-flye.h2-un.arrow-p1.fasta.gz.stats.txt"
    print(reformat(fn))

if __name__ == '__main__':
    main()
