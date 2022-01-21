- Per-haplotype bench to GIAB HG002

bash per_hap_bench.sh hg19.fa giab.vcf.gz giab.include.bed NA24385.exact.intramerge.vcf.gz

- Simplest case of SV merging

bash simplest_case.sh hg19.fa NA24385.exact.intramerge.vcf.gz
-> Figure2a uses this data

- At this point, need to have run "Make single sample summary stats" from base directory

- Merges to GIAB
bash merges_to_giab.sh hg19.fa giab.vcf.gz giab.include.bed exact.vcf.gz strict.vcf.gz 

- Figure2b
I need - sample, reference, merge, svtype for all.
Then I can do the counts, for this section as well as all the plots.

Though I also need het/hom ratio data pulled out somewhere... dangit or maybe its in the df

Script to make the dataframe (I think I already have it), but it might be too big
Clean Intra-Sample notebook

- Exact count and haplotype comparison
% similarity and stuff
Need to make that data

- Three merges against GIAB HG002
Just make dataframes
Then table maker

- All 36 Samples, Average per-sample, reference views
Het/Hom Ratios

- 
	
	
