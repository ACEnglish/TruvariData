Most of the tasks to create the data can be done fairly simply just by organizing your
inputs and using something like:

`find data/ -name "exact.vcf.gz" | xargs -I {} -P 4 bash single_sample_merge.sh {} reference.fa`

As an example, here are other scripts I've made to help speed up the processing


# Making all the exact.vcf.gz in one go

Make an input tab-separated file tracking haplotype fastas as pairs with columns:

- samp_name - the name of the sample
- project - the name of the project
- hap1 - haplotype1.fasta
- hap2 - haplotype2.fasta

Then, from a reference directory (`e.g. data/hg19/`) you can create a bunch of scripts, each one will call mapping.sh twice and merge.sh
at the end, placing your results in `\`pwd\`/${project}/${samp_name}/exact.vcf.gz`
```
bash make_all_mapping_jobs.sh input.tracking.txt reference.fa
```

You can then make a bunch of cluster jobs using `bash mass_submit.sh` where it will look
for all the newly created jobs.sh files and echo out qsub submission commands

This process will leave a lot of temporary files in the `pwd` that can be removed via:

```
rm -rf *.vcf.gz* *.paf
```
