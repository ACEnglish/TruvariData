"""
Given a file with metadata and log files from the outputs of mapping.sh
Parse the stats files for assembly stats and make a dataframe

input file format tab-delimited
project sample hap ref logfile
"""
import sys
import pandas as pd
import joblib
from collections import OrderedDict

def parse_log(fn):
    data = OrderedDict()
    with open(fn) as fh:
        for line in fh:
            if line.startswith("["):
                continue
            if line.startswith("Number"):
                line = line[len("Number of "):].split(':')
                line[1] = int(line[1].strip())
                data[line[0]] = line[1]
            else:
                if ';' in line:
                    sub, ts = line.split(';')
                    sub = sub.split(' ')
                    sub[0] = int(sub[0])
                    data[sub[1]] = sub[0]
                    ts = ts.split('=')
                    data[ts[0].strip()] = float(ts[1])
                else:
                    idx = line.index(' ')
                    cnt = int(line[:idx])
                    name = line[idx:].strip()
                    data[name] = cnt
    return pd.DataFrame([data])

def main():
    rows = []
    in_file, out_jl = sys.argv[1:]
    with open(in_file) as fh:
        for line in fh:
            proj, samp, hap, ref, fn = line.strip().split('\t')
            data = parse_log(fn)
            data["project"] = proj
            data["sample"] = samp
            data["hap"] = hap
            data["reference"] = ref
            rows.append(data)
    data = pd.concat(rows)
    joblib.dump(data, out_jl)

def test():
    log = "/stornext/snfs4/next-gen/scratch/english/round2/insertion_ref/long_read_data/remap/logs/chm13.draft_v1.0.fasta__v12_NA19238_hgsvc_pbsq2-clr_1000-flye.h2-un.arrow-p1.fasta.gz.sh.log"
    pd.options.display.max_columns = None
    print(parse_log(log))

if __name__ == '__main__':
    main()
