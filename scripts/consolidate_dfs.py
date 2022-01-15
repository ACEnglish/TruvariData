import sys
import joblib
import pandas as pd

files = [("Exact", "exact.sv.jl", "exact.CBGcoords.anno.jl"),
         ("Truvari", "truvari.svs.jl", "truvari.CBGcoords.anno.jl"),
         ("Jasmine", "jasmine.af.svs.jl", "jasmine.af.CBGcoords.anno.jl"),
         ("Naive", "naive.svs.jl", "naive.CBGcoords.anno.jl"),
         ("SURVIVOR", "survivor.1000.svs.jl", "survivor.1000.CBGcoords.anno.jl")]

parts = []
for name, var_fn, anno_fn in files:
    v = joblib.load(var_fn)
    v["AF"] = v["AF"].apply(lambda x: x[0])
    a = joblib.load(anno_fn)
    a.set_index("vcf_key", inplace=True)
    view = a.join(v[["svtype", "AF"]])
    view["merge"] = name
    parts.append(view)

joblib.dump(pd.concat(parts), "CBGcoords.data.jl")
