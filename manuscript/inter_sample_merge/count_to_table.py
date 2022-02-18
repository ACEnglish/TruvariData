import sys
import pandas as pd
count = sys.argv[1]
af = sys.argv[2]
rows = []
with open(count, 'r') as fh:
    while True:
        name = fh.readline().strip()
        dels = fh.readline().strip()
        inss = fh.readline().strip()
        if name == "":
            break
        name = name.split('/')
        d = int(dels.split(' ')[0])
        i = int(inss.split(' ')[0])
        rows.append([name[1], name[2].split('.')[0], d, i])

data = pd.DataFrame(rows, columns=["reference", "merge", "del_cnt", "ins_cnt"])
data['tot_cnt'] = data['del_cnt'] + data['ins_cnt']
data.set_index(['reference', 'merge'], inplace=True)

data['tot_af'] = None
data['del_af'] = None
data['ins_af'] = None
with open(af, 'r') as fh:
    while True:
        name = fh.readline().strip()
        tot = fh.readline().strip()
        dels = fh.readline().strip()
        inss = fh.readline().strip()
        if name == "":
            break
        name = name.split('/')
        ref = name[1]
        merge = name[2].split('.')[0]
        tot = float(tot)
        dels = float(dels)
        inss = float(inss)
        data.loc[(ref, merge), 'tot_af'] = tot
        data.loc[(ref, merge), 'del_af'] = dels
        data.loc[(ref, merge), 'ins_af'] = inss

print(data)       
data.reset_index(inplace=True)
data.to_csv("SV_count_af_summary.tsv", index=False, sep='\t')

