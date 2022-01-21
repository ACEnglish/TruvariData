import joblib
import pandas as pd

hap1 = joblib.load("data/hg002_hap1/data.jl")
hap2 = joblib.load("data/hg002_hap2/data.jl")

cat = pd.concat([hap1, hap2])
joblib.dump(cat, "data/hg002_haps_sim.jl")
view = cat[cat["state"] == 'tp']

high_sim = (view["PctSeqSimilarity"] >= 0.95) \
         & (view["PctSizeSimilarity"] >= 0.95) 


print("pct >= 95%% sim: %.1f" % (high_sim.sum() / len(view) * 100))

state = cat["state"].value_counts()
print("ppv = %.2f" % (state['tp'] / (state['tp'] + state['fp'])))
