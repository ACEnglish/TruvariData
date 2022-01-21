# per-hap bench to GIAB
set -e

# SET msru/scripts dir for reusing stuff
# Currently relative to here
MSRUSRC=../../scripts/
REF=$1
GIABVCF=$2
GIABBED=$3

# NA24385 hg19 exact merged VCF
LR_EXACT_VCF=$4

mkdir -p data
# Turn LR into per-hap VCF
python $MSRUSRC/only_svs.py $LR_EXACT_VCF | grep -e "^#\|1/0$\|1/1$" | bgzip > data/hap1.vcf.gz
tabix data/hap1.vcf.gz

python $MSRUSRC/only_svs.py $LR_EXACT_VCF | grep -e "^#\|0/1$\|1/1$" | bgzip > data/hap2.vcf.gz
tabix data/hap2.vcf.gz

truvari bench -f $REF -b $GIABVCF --passonly --includebed $GIABBED --multimatch -c data/hap1.vcf.gz -o data/hg002_hap1
truvari vcf2df -i -b data/hg002_hap1 data/hg002_hap1/data.jl

truvari bench -f $REF -b $GIABVCF --passonly --includebed $GIABBED --multimatch -c data/hap2.vcf.gz -o data/hg002_hap2
truvari vcf2df -i -b data/hg002_hap2 data/hg002_hap2/data.jl

python per_hap_bench_summary.py
