import sys
import pysam
import joblib
import pandas as pd
import truvari


in_vcf = sys.argv[1]

data = truvari.vcf_to_df(in_vcf, sample=0)
data = data[[_ for _ in data.columns if _ != "GT"]]

v = pysam.VariantFile(in_vcf)
per_sample_gt = {_:[] for _ in v.header.samples}

for entry in v:
    for sample in v.header.samples:
        per_sample_gt[sample].append(truvari.get_gt(entry.samples[sample]["GT"]).name)
for sample in per_sample_gt:
    per_sample_gt[sample] = pd.Series(per_sample_gt[sample], name="GT", index=data.index)
joblib.dump({"variants": data, "genotypes":per_sample_gt}, sys.argv[2])
