

mkdir -p data
function query() {
bcftools query -f "%CHROM\t%POS\t%INFO/NeighId\t%INFO/SVLEN\t%INFO/SVTYPE\t%INFO/TRFcopies\t%INFO/TRFDiff\t%INFO/TRFrepeat\t%ALT\n" \
    -i "TRF == 1" $1 | sort -k3,3V -k7,7n
}

query ../inter_sample_merge/data/grch38/exact.vcf.gz | gzip > data/exact.trf.txt.gz
#query ../inter_sample_merge/data/grch38/jasmine.vcf.gz | gzip > data/jasmine.trf.txt.gz
#query ../inter_sample_merge/data/grch38/naive.vcf.gz | gzip > data/naive.trf.txt.gz
#query ../inter_sample_merge/data/grch38/survivor.vcf.gz | gzip > data/survivor.trf.txt.gz
#query ../inter_sample_merge/data/grch38/truvari.vcf.gz | gzip > data/truvari.trf.txt.gz
