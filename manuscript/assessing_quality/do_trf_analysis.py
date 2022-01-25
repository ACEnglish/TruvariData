import sys
import joblib
import hashlib
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

def load_txt(fn):
    d = pd.read_csv(fn, sep="\t", header=None)
    d.columns = ["CHROM", "POS", "NeighId", "SVLEN", "SVTYPE",
                 "TRFcopies", "TRFDiff", "TRFrepeat", "ALT"]
    def mk_key(line):
        result = hashlib.md5(f"{line['CHROM']} {line['POS']} {line['ALT']} {line['SVTYPE']}".encode())
        return result.hexdigest()

    d = d[(d["SVTYPE"] == 'INS') & (d["TRFDiff"] != ".")]
    d["var key"] = d.apply(mk_key, axis=1)
    d["TRFDiff"] = d["TRFDiff"].astype(float)
    d.set_index("var key", inplace=True)
    return d

def make_summary(base, other):
    cmp = base.join(other, rsuffix='cmp')
    parts = []
    for pos, i in enumerate(cmp.groupby(["NeighId", "TRFrepeat"])):
        base = i[1]["TRFDiff"].value_counts()
        other = i[1]["TRFDiffcmp"].value_counts(dropna=False)
        view = pd.concat([base, other], axis=1)
        view.reset_index(inplace=True)
        view.columns = ["copynum", "exactcnt", "othercnt"]
        view["loc key"] = pos
        parts.append(view)
    data = pd.concat(parts)
    rows = []
    for key, ck in data.groupby("loc key"):
        rows.append([key, 
                     (~ck["exactcnt"].isna()).sum(),
                     (ck["exactcnt"] > 1).sum(),
                     len(ck[(ck["othercnt"] > 1) & (~ck["exactcnt"].isna())]),
                     (ck["othercnt"].isna()).sum()])
    sum_dat = pd.DataFrame(rows, columns=["loc key", 
                                          "exact_cn_cnt",
                                          "exact_redund_vars",
                                          "other_redund_vars",
                                          "other_missing_cnt"]
                          )
    return sum_dat


exa = load_txt("data/exact.trf.txt.gz")
tru = load_txt("data/truvari.trf.txt.gz")
jas = load_txt("data/jasmine.trf.txt.gz")
sur = load_txt("data/survivor.trf.txt.gz")
nav = load_txt("data/naive.trf.txt.gz")

tru_sum = make_summary(exa, tru)
jas_sum = make_summary(exa, jas)
sur_sum = make_summary(exa, sur)
nav_sum = make_summary(exa, nav)

print("Total TR Loci", len(tru_sum["exact_redund_vars"]))
non_redund = tru_sum[tru_sum["exact_redund_vars"] == 0]
print("Non-Redundant Sites:", len(non_redund))
print("Non-Redundant Num Variants:", non_redund["exact_cn_cnt"].sum())

has_redund = tru_sum[tru_sum["exact_redund_vars"] != 0]
print("Redund Sites:", len(has_redund))
print("Redund Num Variants:", has_redund[["exact_redund_vars", "exact_cn_cnt"]].sum().sum())

print("# Redund summary")
redund_data = []
for name, i in [("Truvari", tru_sum), ("Jasmine", jas_sum), ("SURVIVOR", sur_sum), ("Naive", nav_sum)]:
    p = i[i["exact_redund_vars"] != 0][["other_redund_vars"]]
    p["name"] = name
    redund_data.append(p)
redund_data = pd.concat(redund_data).reset_index()
redund_data["redund_bins"] = pd.cut(redund_data["other_redund_vars"], [0, 1, 100], 
                               labels=["None", "Any"], right=False)

redund_data.columns = ['index', 'other_redund_vars', 'Merge', 'redund_bins']
print(redund_data.groupby(['Merge', 'redund_bins']).size().unstack())

print("# Missing summary")
missing_data = []
for name, i in [("Truvari", tru_sum), ("Jasmine", jas_sum), ("SURVIVOR", sur_sum), ("Naive", nav_sum)]:
    p = i[i["exact_redund_vars"] != 0][["other_missing_cnt"]]
    p["name"] = name
    missing_data.append(p)
missing_data = pd.concat(missing_data).reset_index()

print(missing_data.groupby(["name"])["other_missing_cnt"].describe(percentiles=[0.5, 0.99]).sort_values('mean'))

print("# Percent without missing")
for i in missing_data['name'].unique():
    v = missing_data[missing_data['name'] == i]
    t = v['other_missing_cnt'].value_counts()[0] 
    print (i, "%.1f" % (t / len(v) * 100))

joblib.dump(redund_data, 'redund_data.jl', compress=9)
joblib.dump(missing_data, 'missing_data.jl', compress=9)

