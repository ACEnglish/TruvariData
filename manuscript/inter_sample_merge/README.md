Needs the inter-merge VCFs created as well as other-merges.

Organize them inside data/<reference>/<program>.vcf.gz

Make sure annotations are on them
truvari anno trf
truvari anno Repmask
truvari anno bpovl [tbd]
bcftools +fill-tags

I'm just going to keep these as the final versions. The other directories are temporary working dirs that I can just
remove

# Basic stats
bash make_stat_files.sh

``
