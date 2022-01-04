import sys
import allel
import joblib
import scipy.spatial
import numpy as np
import pandas as pd
import pysam
in_vcf = sys.argv[1]
out_df = sys.argv[2]
in_vcf_file = sys.argv[3]

p_vcf = pysam.VariantFile(in_vcf_file)
samples = [_.split('_')[-1] for _ in p_vcf.header.samples]
print(samples)
vcf = allel.read_vcf(in_vcf)
tg = allel.GenotypeArray(vcf["calldata/GT"])

# Singleton / LD removal
ac = tg.count_alleles()[:]
flt = (ac.max_allele() == 1) & (ac[:, :2].min(axis=1) > 3)
tg_filt = tg.compress(flt, axis=0)
def ld_prune(gn, size, step, threshold=.1, n_iter=1):
    for i in range(n_iter):
        loc_unlinked = allel.locate_unlinked(gn, size=size, step=step, threshold=threshold)
        n = np.count_nonzero(loc_unlinked)
        n_remove = gn.shape[0] - n
        print('iteration', i+1, 'retaining', n, 'removing', n_remove, 'variants')
    return loc_unlinked
gn = tg_filt.to_n_alt()
loc_unlinked = ld_prune(gn, size=100, step=20, threshold=.1, n_iter=1)
tg_filt_ld = tg_filt.compress(loc_unlinked, axis=0)

#td = allel.pairwise_distance(tg_filt_ld.to_n_alt(), metric='jensenshannon')
td = allel.pairwise_distance(tg.to_n_alt(), metric='jensenshannon')
sq = scipy.spatial.distance.squareform(td)
a = pd.DataFrame(sq, columns=samples, index=samples)
joblib.dump(a, out_df)
