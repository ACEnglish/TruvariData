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

2) Run density on the long-reads (1kb)
3) Run density on the short-reads (1kb)
4) I need to do the intersections...
5) And then just regioneR





