import joblib

lr = joblib.load("density/lr_grch38_truvari.jl")
sr = joblib.load("density/sr_grch38_truvari.jl")

data = lr.join(sr, rsuffix="_")
view = data[(data["anno"] == 'dense') & (data["anno_"] == 'sparse')]
view[["chrom", "start", "end"]].to_csv("missing_candidates.bed", sep='\t', header=False, index=False)
