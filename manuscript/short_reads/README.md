# Discovery
Should be organized into
`data/discovery/<program>/<sample>.<reference>.vcf.gz`
with long-reads in 
`../inter_sample_merge/data/<reference>/<merge>.vcf.gz`

Need to bench each short-read vcf with each long read merge
```
mkdir -p temp/
mkdir -p jobs/
mkdir -p logs/
python make_bench_jobs.py
# And submit them all
bash work.sh
```
Once they're done, do

```
python summary_consolidate.py
```

Density experiments

1) Need to create the short-read merges
use `bash msru/scripts/short_read_perform_other_merges.sh`

2) Run density
bash make_density.sh
python do_density.py 

4) Do the intersections

```
bcftools query -f "%INFO/SVTYPE\n" -R missing_candidates.bed ../inter_sample_merge/data/grch38/truvari.vcf.gz | sort | uniq -c 
#    6082 DEL
#   17991 INS
bcftools query -f "%INFO/SVTYPE\n" ../inter_sample_merge/data/grch38/truvari.vcf.gz | sort | uniq -c 
#   63418 DEL
#  132287 INS
bedtools intersect -c -a missing_candidates.bed -b ~/scratch/code/truvari/resources/grch38.simpleRepeat.truvari.bed.gz | awk '$4 == 0' | wc -l 
# 360
wc -l missing_candidates.bed 
# 3719 missing_candidates.bed
python -c 'print(1 - 360 / 3719)'
# 0.9031997848884109
```

5) And then just regioneR











