

echo 'exact'
python get_hit_counts.py ../data/grch38/exact.vcf.gz gene_anno/exact.jl
echo 'jasmine'
python get_hit_counts.py ../data/grch38/jasmine.vcf.gz gene_anno/jasmine.jl
echo 'naive'
python get_hit_counts.py ../data/grch38/naive.vcf.gz gene_anno/naive.jl
echo 'survivor'
python get_hit_counts.py ../data/grch38/survivor.vcf.gz gene_anno/survivor.jl
echo 'truvari'
python get_hit_counts.py ../data/grch38/truvari.vcf.gz gene_anno/truvari.jl
