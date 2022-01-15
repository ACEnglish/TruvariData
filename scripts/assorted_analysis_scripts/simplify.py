import sys
import joblib
import pandas as pd
import truvari

is_par = False
samples = ["HG00096", "HG00171", "HG00512", "HG00513", "HG00514", "HG00731",
"HG00732", "HG00733", "HG00864", "HG01114", "HG01505", "HG01596", "HG02011", "HG02492", "HG02587",
"HG02818", "HG03009", "HG03065", "HG03125", "HG03371", "HG03486", "HG03683", "HG03732", "NA12329",
"NA18534", "NA18939", "NA19238", "NA19239", "NA19240", "NA19650", "NA19983", "NA20509", "NA20847"]

def get_gq(pls):
    def srt(x):
        x = [_ for _ in x if _]
        j = sorted(list(x))
        try:
            return j[1] - j[0]
        except IndexError:
            return None
    gqs = pls.apply(srt, axis=1)
    return gqs
            
in_fn, out_fn = sys.argv[1:]
data = joblib.load(in_fn)
keep = ~data.index.str.startswith("chrY") & ~data.index.str.startswith("chrX")
data = data[keep]

desc_columns = ["AF", "MAF", "svtype", "szbin", "REMAP", "NumCollapsed",
                "TRF", "TRFperiod", "TRFcopies", "NumNeighbors"]

main_cols = data[desc_columns]
main_cols["AF"] = main_cols["AF"].apply(lambda x: x[0])
main_cols["MAF"] = main_cols["MAF"].apply(lambda x: x[0])
main_cols["ASMCOVUP"] = data["ASMCOV"].apply(lambda x: x[0])
main_cols["ASMCOVDN"] = data["ASMCOV"].apply(lambda x: x[1])

all_parts = []
for i in samples:
    # Setting the Genotypes to the easier set
    base = data[i +  "_GT"].apply(lambda x: truvari.get_gt(x).name if isinstance(x, tuple) else 'UNK')
    comp = data[i +  "_GT_"].apply(lambda x: truvari.get_gt(x).name if isinstance(x, tuple) else 'UNK')

    view = main_cols.copy()
    view["SAMPLE"] = i
    view["BASE_GT"] = base
    view["COMP_GT"] = comp
    view["AD_ref"] = data[i + "_AD_ref"]
    view["AD_alt"] = data[i + "_AD_alt"]

    if not is_par:
        view["GQ"] = data[i + "_GQ"]
    else:
        cols = [i + '_' + x for x in ["PL_ref", "PL_het", "PL_hom"]]
        view["GQ"] = get_gq(data[cols])
        view["FT"] = data[i + "_FT"].apply(lambda _: "PASS" in _)

    all_parts.append(view)

out = pd.concat(all_parts)

truvari.optimize_df_memory(out)
joblib.dump(out, out_fn, compress=3)

