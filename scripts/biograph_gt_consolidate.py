import os
import sys
import joblib
import truvari
import pandas as pd

def make_biograph_results(in_vcf, base_df):
    """
    Returns results and full from a join/anno of the base/comparison SV vcfs.jl
    """
    comp = truvari.vcf_to_df(in_vcf, True, True)
    
    full = base_df.join(comp, lsuffix="_base", rsuffix="_comp")
    full["GT_base"] = full["GT_base"].apply(lambda x: truvari.get_gt(x).value if isinstance(x, tuple) else np.nan).dropna().astype(int)
    full["GT_comp"] = full["GT_comp"].apply(lambda x: truvari.get_gt(x).value if isinstance(x, tuple) else np.nan).dropna().astype(int)
    full["concordant"] = full["GT_comp"] == full["GT_base"]
    res = full[["GQ", "GT_comp", "GT_base", "concordant", "DP", "svtype_base", "PL_ref", "PL_het", "PL_hom", "NumNeighbors"]]
    res.columns = ["GQ", "predict", "GT_label", "concordant", "DP", "svtype", "REF", "HET", "HOM", "NumNeighbors"]
    res = res.dropna()
    res["predict"] = res["predict"].astype(int)
    res["presence"] = res[["GT_label", "predict"]].apply(presence_compare, axis=1)
    return res, full

def make_paragraph_results(in_vcf, base_df):
    """
    Returns results and full from a join/anno of the base/comparison SV vcfs.jl
    """
    par_comp = truvari.vcf_to_df(in_vcf, False, True)
    chrY = par_comp.index.str.startswith("chrY")
    par_comp.loc[chrY, "PL_hom"] = par_comp.loc[chrY, "PL_het"]
    par_comp.loc[chrY, "PL_het"] = np.nan
    par_comp["GT"] = par_comp["GT"].apply(lambda x: truvari.get_gt(x).name)
    pl_arr = par_comp[['PL_ref', 'PL_het', 'PL_hom']].fillna(value=np.nan).values
    pl_arr.sort(axis=1)
    par_comp["GQ"] = [(row[1] - row[0]) for row in pl_arr]
    par_comp = par_comp.join(base_df, rsuffix="_base")
    par_comp["concordant"] = par_comp["GT"] == par_comp["GT_base"]
    par_comp["presence"] = par_comp[["GT_base", "GT"]].apply(presence_compare, axis=1)
    par_comp["predict_class"] = par_comp[["GT_base", "GT"]].apply(concordance_compare, axis=1)
    return par_comp


base_df = sys.argv[1] # ../data/paragraph_ref/sv_only.df
in_dir = sys.argv[2] # ../data/short_read_calls/genotyping/paragraph/
out_df = os.path.join(in_dir, "results.jl")

base = joblib.load(base_df)
pg_results = []
for i in glob.glob(os.path.join(in_dir, "*.vcf.gz")):
    sample = os.path.basename(i)[:-len(".vcf.gz")]
    results = make_paragraph_results(i, base['genotypes'][sample])
    results['sample'] = sample
    pg_results.append(results)
pg_results = pd.concat(pg_results)
joblib.dump(pg_results, out_df)
