# Create the raw counts

Assumes the data in `../inter_sample_merge` is complete

```
bash trf_table_magic.sh
```
# make the results

```
python do_trf_analysis.py
```
Results:
```
Total TR Loci 20207
Non-Redundant Sites: 11151
Non-Redundant Num Variants: 20071
Redund Sites: 9056
Redund Num Variants: 91500
# Redund summary
redund_bins  None   Any
Merge
Jasmine      6938  2118
Naive        6998  2058
SURVIVOR     9055     2
Truvari      5658  3398
# Missing summary
	   count      mean       std  min  50%   99%    max
name
Truvari   9056.0  1.885159  3.702441  0.0  0.0  19.0   55.0
Jasmine   9056.0  4.430543  6.607730  0.0  2.0  31.0  108.0
Naive     9056.0  5.482774  7.927469  0.0  3.0  37.0  118.0
SURVIVOR  9057.0  7.141548  8.240254  0.0  4.0  40.0  120.0
# Percent without missing
Truvari 52.6
Jasmine 23.5
SURVIVOR 0.7
Naive 20.4
```

