import os
import sys
import joblib
import truvari
import pandas as pd

def presence_compare(vals):
    """
    True or false based on presence
    """
    base, comp = vals.to_list()
    if base == "REF":
        if comp == "REF":
            return "TN"
        else:
            return "FP"
    else:
        if comp == "REF":
            return "FN"
        else:
            return "TP"

def concordance_compare(vals):
    """
    True/False based on concordance
    """
    base, comp = vals.to_list()
    if base == "REF":
        if comp == "REF":
            return "TN"
        else:
            return "FP"
    elif base == "HET":
        if comp == "REF":
            return "FN"
        if comp == "HET":
            return "TP"
        else:
            return "FP"
    elif base == "HOM":
        if comp == "REF":
            return "FN"
        if comp == "HET":
            return "FP"
        else:
            return "TP"

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

def make_biograph_results(in_vcf, base_df):
    """
    Returns results and full from a join/anno of the base/comparison SV vcfs.jl
    """
    par_comp = truvari.vcf_to_df(in_vcf, False, True)
    par_comp["GT"] = par_comp["GT"].apply(lambda x: truvari.get_gt(x).name)
    par_comp = par_comp.join(base_df, rsuffix="_base")
    par_comp["concordant"] = par_comp["GT"] == par_comp["GT_base"]
    par_comp["presence"] = par_comp[["GT_base", "GT"]].apply(presence_compare, axis=1)
    par_comp["predict_class"] = par_comp[["GT_base", "GT"]].apply(concordance_compare, axis=1)
    return par_comp


base_df = sys.argv[1] # ../data/paragraph_ref/sv_only.df
method = sys.argv[2] # paragraph | biograph
out_df = sys.argv[3] #
in_vcfs = sys.argv[4:]

if method not in ["paragraph", "biograph"]:
    print("method should be paragraph or biograph")
    exit(1)

base = joblib.load(base_df)
all_results = []
for i in in_vcfs:
    if method == "paragraph":
        sample = os.path.basename(i)[:-len(".vcf.gz")]
        reference = "grch38"
        results = make_paragraph_results(i, base['genotypes'][sample])
    elif method == "biograph":
        dat = i.split('/')
        sample = dat[-2]
        reference = dat[-1].split('.')[0]
        results = make_biograph_results(i, base['genotypes'][sample])
    results['sample'] = sample
    results["reference"] = reference
    all_results.append(results)
results = pd.concat(all_results)
joblib.dump(results, out_df)
