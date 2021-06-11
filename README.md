# msru

Investigating maximum short-read utility for structural variation

This repository contains the workflow and notes for creating most of the data for this research

# References

Subset references to only Autosomes and X/Y.
GRCh38
hg19
t2t chm13 v1.0


# Creating the per-sample SV calls


## File structure:

The per-sample vcfs are organized into sub-directories by `reference/project/sample`
(e.g. `chm13/li/NA12878.vcf.gz`)

## Download haplotype fastas
The haplotype fasta files are pulled from their public locations using `eichler_download.sh` and `li_download.sh`

## Haplotype mapping and variant calling
Map each sample to a reference and call variants using mapping.sh

  `bash mapping.sh haplotype.1.fasta sample.hap1 reference.fasta`

This creates an alignment file `sample.hap1.paf`, a vcf file `sample.hap1.var.vcf.gz`, and an index for that vcf.

## Merge haplotypes
Merge the two haplotype vcf files together using
  
  `bash merge_haps.sh sample.hap1.var.vcf.gz sample.hap2.var.vcf.gz sample`

This creates a diploid vcf file name `sample.vcf.gz` and its index.

## Making per-sample collapsed VCFs

Make a file like `single_sample.txt` with each single-sample VCF.
Run `bash per_sample_collapse.sh` to do the strict and loose collapsing of per-sample
files. This will create single-sample `exact_merge` and `loose_merge` in each reference
directory. 

## Making multi-sample VCFs

Run `multi_merge.sh`
Be sure to update the TMPDIR and reference file variables in the script
Run this in a reference destination directory / merge strategy (e.g. grch38/exact_merge)
And provide G as first argument to make the grch38 version, else chm13 is used

## Make summary stats


##
*Note: at this point, multiple vcfs were created and organized in a directory structure:*
TODO: Fill in the directory structure 
TODO: Resume processing for stats and stuff here
