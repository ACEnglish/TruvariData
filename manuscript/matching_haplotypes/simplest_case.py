import joblib

data = joblib.load("data/compare_haps/data.jl")

view = data[data["state"].isin(["tp", "fp", "fn"])]

high_sim = (view["PctSeqSimilarity"] > 0.95) \
         & (view["PctSizeSimilarity"] > 0.95) 

print("> 95%% sim: %d" % (high_sim.sum()))


some_sim = (view["PctSeqSimilarity"].between(0.70, 0.95)) \
         & (view["PctSizeSimilarity"].between(0.70, 0.95))

print("(70, 95) sim: %d" % (some_sim.sum()))






