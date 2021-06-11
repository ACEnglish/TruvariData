# msru

Investigating maximum short-read utility for structural variation

This repository contains the workflow and notes for creating most of the data for this research

# Requirements:

bcftools
truvari
minimap
paftools
paragraph
biograph.. eventually

# References

Subset references to only Autosomes and X/Y.
GRCh38
hg19
t2t chm13 v1.0

# Creating the per-sample SV calls

## Download haplotype fastas
The haplotype fasta files are pulled from their public locations using `eichler_download.sh` and `li_download.sh`

## Haplotype mapping and variant calling
Map each sample to a reference and call variants using mapping.sh

  `bash mapping.sh haplotype.1.fasta sample.hap1 reference.fasta`

This creates an alignment file `sample.hap1.paf`, a vcf file `sample.hap1.var.vcf.gz`, and an index for that vcf.

## Merge haplotypes
Merge the two haplotype vcf files together using
  
  `bash merge.sh sample.hap1.var.vcf.gz sample.hap2.var.vcf.gz sample`

This creates a diploid vcf file name `sample.vcf.gz` and its index. This is the start of
our 'exact' merge VCFs. At this point, the files should be orgainzed in the below file
structure

## File structure:

The per-sample vcfs are organized into sub-directories starting with the exact vcf path
`data/reference/project/sample/merge_strategy/` (e.g. `data/chm13/li/NA12878/exact.vcf.gz`)
Be sure to make have the index present, also

## Making per-sample collapsed VCFs

Run per-sample strict/exact collapsing using:
```bash
	single_sample_collapse.sh $exact_vcf_path reference.fa
```
Where `$exact_vcf_path` is described above in File Structure.

This will run `truvari collapse` for exact and for loose merging and place them
in the appropriate directory. For example `data/chm13/li/NA12878/strict.vcf.gz` 

Each collapse also produces `removed.strict.vcf.gz`, vcf indexes, and logs in `collapse.strict.log`

## Making multi-sample VCFs

Once all of the samples have been processed, the script `multi_merge.py` will parse the
samples and create the commands do the joint merging.

```bash
python multi_merge.py --reference path/to/reference.fa  chm13/*/*/strict.vcf.gz > merge_chm13.sh
bash merge_chm13.sh
```

This will find all of the chm13 vcfs, build the appropriate header, and the commands to
create the exact, strict, and loose multi-sample merges.

These multi sample merges are placed inside of the `data/reference/` directory (e.g.
`data/chm13/exact.loose.vcf.gz`

Where the exact is the intra-sample merging strategy and loose is the inter-sample merging
strategy.

## Build the pararaph multi-sample VCFs

build_paragraph.sh data/chm13/exact.exact.vcf.gz

## Make summary stats

Beside a VCF, create a joblib DataFrame of just SVs >= 50bp using, for example:

`bash make_stats.sh data/chm13/exact.vcf.gz`

Once these are all created, run
`python consoidate_stats.py -o sv_stats.jl data/`

This will look for all subdirectories that have subdirectories that have subdirectories
containing '.jl' files. (a.k.a. reference/project/sample/merge_strategy.jl)
So that it can append columns of those path metadata information to each row, drop the
index, and make a usable dataframe for the SVCharacteristics notebook.

