Needs the inter-merge VCFs created as well as other-merges.

Organize them inside data/<reference>/<program>.vcf.gz

Make sure annotations are on them
truvari anno trf
truvari anno Repmask
bcftools +fill-tags

I'm just going to keep these as the final versions. The other directories are temporary working dirs that I can just
remove

# Basic stats
bash make_stat_files.sh

# Summary figure stats
python pvcf_byty_stats.py data/*/*.vcf.gz


# Med Genes
see `med_genes`

# Mendelian
python mendelian_checker.py
