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
  
  `bash merge_haps.sh sample.hap1.var.vcf.gz sample.hap2.var.vcf.gz sample`

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

## Make single sample summary stats

Beside a VCF, create a joblib DataFrame of just SVs >= 50bp using, for example:

`bash make_stats.sh data/chm13/exact.vcf.gz`

Once these are all created, run
`python consolidate_stats.py data/ stats/single_sample_stats.jl`

This will look for all subdirectories that have subdirectories that have subdirectories
containing '.jl' files. (a.k.a. reference/project/sample/merge_strategy.jl)
So that it can append columns of those path metadata information to each row, drop the
index, and make a usable dataframe for the SVCharacteristics notebook.

## Making multi-sample VCFs

File structure:
In a directory, not the same as the single-sample (`data/` used above), we will create
all the combinations of merges. For a single reference, we need to take all the exact 
merges and then do an exact merge to create `exact.exact.vcf.gz`

Do this by calling:
```bash
python multi_merge.py in_dir out_dir reference.fa > the_merge_script.sh
```

This will create all the commands needed to make all combinations of merges inside of
```
out_dir/exact/exact.vcf.gz
out_dir/exact/strict.vcf.gz
out_dir/loose/strict.vcf.gz
etc ...
```
## Multi-sample stats

Once all of the samples have been processed, create the stats via:
```
python only_svs.py input.vcf.gz | truvari truv2df -v -i -f /dev/stdin output.jl
```

Consolidate the stats with `python merge_stast.py *.jl` where  `*.jl` are all
from  one of `out_dirs` made during the multi-sample merge step. Note that 
this assumes that `out_dir` is the name of a reference.

## Build the paragraph multi-sample VCFs

Given one of the multi-sample merges, create a paragraph reference out of only the svs using:

```bash
 bash run_paragraphs.sh data/multi_merge/hg19/strict/strict.vcf.gz \
 						data/reference/hg19/hg19.fa \
						data/paragraph/hg19
```

This will try to run paragraph just enough to make the reference inputs needed to run a
modified version of paragraph https://github.com/ACEnglish/paragraph


## Benchmarking single-sample discovery
ABCDE

## Other merges

To compare other merging methods, we made a custom script `naieve_50.py` to do 50%
reciprocal overlap merging. We then downloaded three other SV merging tools to compare.

SURVIVOR v1.0.6 https://github.com/fritzsedlazeck/SURVIVOR
Jasmine v1.1 https://github.com/mkirsche/Jasmine
svimmer v0.1 https://github.com/DecodeGenetics/svimmer

Using the strict intra-sample merge SVs, we ran each program with default parameters.

```
SURVIVOR merge grch38_plain.txt 500 1 1 0 1 50 survivor.vcf
run.sh file_list=grch38_plain.txt out_file=jasmine.vcf threads=48
python svimmer --threads 48 grch38_gzip.txt \
	$(for i in $(seq 1 22) X Y; do echo -n chr$i " "; done) > svimmer.vcf
```

AFs were measured using `bcftools +fill-tags`
Jasmine and svimmer don't preserve genotype information from the input VCFs, so AF
couldn't be measured

