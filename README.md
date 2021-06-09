# msru

Investigating maximum short-read utility for structural variation

This repository contains the workflow and notes for creating most of the data for this research

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

This creates a diploid vcf file name `sample.vcf.gz` and its index.

*Note: at this point, multiple vcfs were created and organized in a directory structure:*
TODO: Fill in the directory structure 
TODO: Resume processing for stats and stuff here
