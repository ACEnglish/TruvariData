set -e


MSRUSRC=/users/u233287/scratch/insertion_ref/msru/scripts/
# hg19 NA24385 exact vcf
REF=$1
LR_EXACT_VCF=$2

mkdir -p data/
#python $MSRUSRC/only_svs.py $LR_EXACT_VCF > data/exact.vcf
echo "Identical Sequence" $(grep -c "1/1$" data/exact.vcf)

echo "Remaining " $(grep -vc "1/1$" data/exact.vcf)

grep -e "^#\|1/0$" data/exact.vcf | bgzip > data/hap1.vcf.gz
tabix data/hap1.vcf.gz
grep -e "^#\|0/1$" data/exact.vcf | bgzip > data/hap2.vcf.gz
tabix data/hap2.vcf.gz

truvari bench -b data/hap1.vcf.gz -c data/hap2.vcf.gz -f $REF -o data/compare_haps
truvari vcf2df -i -b data/compare_haps/ data/compare_haps/data.jl

python simplest_case.py


