set -e
MSRUSRC=../../scripts/
REF=$1
GIABVCF=$2
GIABBED=$3
EXACT=$4
STRICT=$5
LOOSE=$6
ASMBED_hap1=$7
ASMBED_hap2=$8

mkdir -p data

truvari bench -f $REF -b $GIABVCF --passonly --includebed $GIABBED --multimatch -c $EXACT -o data/exact_bench/
truvari vcf2df -i -b data/exact_bench/ data/exact_bench/data.jl
truvari bench -f $REF -b $GIABVCF --passonly --includebed $GIABBED --multimatch -c $STRICT -o data/strict_bench/
truvari vcf2df -i -b data/strict_bench/ data/strict_bench/data.jl
truvari bench -f $REF -b $GIABVCF --passonly --includebed $GIABBED --multimatch -c $LOOSE -o data/loose_bench/
truvari vcf2df -i -b data/loose_bench/ data/loose_bench/data.jl

# Manually pull recall from summary.txt
echo -e "exact\t$(python summary_to_tsv.py data/exact_bench/summary.txt)"
echo -e "strict\t$(python summary_to_tsv.py data/strict_bench/summary.txt)"
echo -e "loose\t$(python summary_to_tsv.py data/loose_bench/summary.txt)"
# Turn summary.txt into a table, paste into supplementary table 1

# Pct FP/FN without call within 1kbp
echo "FP without a call within 1kbp"
bcftools query -f "\n" -i "TruScore == '.'" data//strict_bench/fp.vcf  | wc -l
grep -vc "#" data/strict_bench/fp.vcf

echo "FN without a call within 1kbp"
bcftools view -i "TruScore == '.'" data//strict_bench/fn.vcf  > data/fn_noneigh.vcf
grep -vc "#" data/fn_noneigh.vcf
bcftools query -f "%INFO/SVTYPE\n" data/fn_noneigh.vcf | sort | uniq -c

echo "FN without aligned coverage2"
vcf_compress data/fn_noneigh.vcf
awk '$4 == 0' $ASMBED_hap1 > data/hap1_nocov.bed
awk '$4 == 0' $ASMBED_hap2 > data/hap2_nocov.bed

cat data/hap1_nocov.bed data/hap2_nocov.bed \
    | bedtools sort -i - \
    | bedtools merge -i - > data/nocov_hg002.bed

bcftools query -f "\n" data/fn_noneigh.vcf.gz -R data/nocov_hg002.bed | wc -l

echo "FN without aligned coverage2"
bash $MSRUSRC/vcf_compress.sh data/strict_bench/fn.vcf
bcftools query -f "%INFO/SVTYPE\n" data/strict_bench/fn.vcf.gz
bcftools view -R data/hap1_nocov.bed data/strict_bench/fn.vcf.gz | bgzip > data/hap1_nocov.vcf.gz
bcftools view -R data/hap2_nocov.bed data/strict_bench/fn.vcf.gz | bgzip > data/hap2_nocov.vcf.gz
truvari consistency data/hap1_nocov.vcf.gz data/hap2_nocov.vcf.gz

echo "Large enrichment"
echo "big missed"
bcftools query -f '\n' -i "SVLEN >= 5000 | SVLEN <= -50000" data/strict_bench/fn.vcf.gz | wc -l
echo "small missed"
bcftools query -f '\n' -i "SVLEN < 5000 & SVLEN > -50000" data/strict_bench/fn.vcf.gz | wc -l
echo "big captured"
bcftools query -f '\n' -i "SVLEN >= 5000 | SVLEN <= -50000" data/strict_bench/tp-base.vcf | wc -l
echo "small captured"
bcftools query -f '\n' -i "SVLEN < 5000 & SVLEN > -50000" data/strict_bench/tp-base.vcf | wc -l
echo "plug these into https://www.socscistatistics.com/tests/fisher/default2.aspx"

