- Per-haplotype bench to GIAB HG002

bash per_hap_bench.sh hg19.fa giab.vcf.gz giab.include.bed NA24385.exact.intramerge.vcf.gz

- Simplest case of SV merging

bash simplest_case.sh hg19.fa NA24385.exact.intramerge.vcf.gz
-> Figure2a uses this data

- At this point, need to have run "Make single sample summary stats" from base directory

- Merges to GIAB
bash merges_to_giab.sh hg19.fa giab.vcf.gz giab.include.bed exact.vcf.gz strict.vcf.gz 

- The rest:
Run `Figures.ipynb`
Set the metadata.txt path and the single_stats.jl from basedir README
