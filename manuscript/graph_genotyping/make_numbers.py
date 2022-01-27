import sys
import joblib
import pandas as pd

in_name, out_table = sys.argv[1:]
data = joblib.load(in_name)
min_coverage = 10
# Refine columns
data["TRF"] = data["TRF"].where(~data["TRF"].isna(), False)
data["state"] = data["BASE_GT"] == data["COMP_GT"]
data["DP"] = data["AD_ref"] + data["AD_alt"]

print("Percent of sites by genotype")
print(data['BASE_GT'].value_counts() / len(data))

# Paragraph Filtering
keep = (data["DP"] >= min_coverage) & (data["FT"]) & (data["COMP_GT"].isin(["REF", "HET", "HOM"]))

# BioGraph Filtering
#keep = (data["DP"] >= min_coverage) & (data["COMP_GT"].isin(["REF", "HET", "HOM"]))
print("Percent of sites filtered %.1f%%" % ( (1 - keep.sum() / len(data)) * 100))

print("# Per-sample TP percent (all)")
print(data[data["BASE_GT"] != "REF"].groupby(['SAMPLE'])['state'].mean().describe())
print("# Per-sample TP percent (filtered)")
print(data[keep & (data["BASE_GT"] != "REF")].groupby(['SAMPLE'])['state'].mean().describe())

print("# Per-sample TN percent (all)")
print(data[data["BASE_GT"] == "REF"].groupby(['SAMPLE'])['state'].mean().describe())
print("# Per-sample TN percent (filtered)")
print(data[keep & (data["BASE_GT"] == "REF")].groupby(['SAMPLE'])['state'].mean().describe())

print("# And there's a difference in accuracy by the BASE GT type")
print(data[keep].groupby(['SAMPLE', 'BASE_GT'])['state'].mean().unstack().describe())

print("Make summary table")
rows = []
all_filter = ('TOT', data['svtype'].isin(["DEL", "INS"]))
del_filter = ('DEL', data['svtype'] == 'DEL')
ins_filter = ('INS', data['svtype'] == 'INS')

all_neigh_filter = ('.', data["NumNeighbors"] != -23)
non_neigh_filter = ("None", data["NumNeighbors"] == 0)
has_neigh_filter = ("Any", data["NumNeighbors"] != 0)

for label1, sv_filt in [all_filter, del_filter, ins_filter]:
    for label2, neigh_filt in [all_neigh_filter, non_neigh_filter, has_neigh_filter]:
        view = data[keep & sv_filt & neigh_filt]
        sv_percent = len(view) / len(data[keep])
        overall_accuracy = view["state"].mean()
        ref_accuracy = view[view["BASE_GT"] == 'REF']["state"].mean()
        alt_accuracy = view[view["BASE_GT"] != 'REF']['state'].mean()
        rows.append([sv_percent, label1, label2, overall_accuracy, ref_accuracy, alt_accuracy])

summary = pd.DataFrame(rows, columns=["pct of sites", "svtype", "NumNeighbors", "Overall", "Reference", "Alternate"])
print(summary)
summary.to_csv(out_table, sep='\t', index=False)
