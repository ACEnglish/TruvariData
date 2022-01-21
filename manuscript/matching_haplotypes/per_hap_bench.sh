# per-hap bench to GIAB

# SET msru/scripts dir for reusing stuff
# Currently relative to here
MSRUSRC=../../scripts/
REF=$1
GIABVCF=$2
GIABBED=$3

# NA24385 hg19 exact merged VCF
LR_EXACT_VCF=$4

# Turn LR into per-hap VCF
hap1_vcf=hap1.vcf.gz
hap2_vcf=hap2.vcf.gz
python $MSRUSRC/only_svs.py $LR_EXACT_VCF | grep -e "1/0$\|1/1$" | bgzip > hap1.vcf
bash $MSRUSRC/vcf_compress.sh hap1.vcf

python $MSRUSRC/only_svs.py $LR_EXACT_VCF | grep -e "0/1$\|1/1$" | bgzip > hap2.vcf
bash $MSRUSRC/vcf_compress.sh hap2.vcf

truvari bench -b $GIABVCF --passonly --includebed $GIABBED --multimatch -c $hap1_vcf -o hg002_hap1
truvari vcf2df -b hg002_hap1 hg002_hap1/data.jl

truvari bench -b $GIABVCF --passonly --includebed $GIABBED --multimatch -c $hap2_vcf -o hg002_hap2
truvari vcf2df -b hg002_hap2 hg002_hap2/data.jl

# Numbers can be pulled from dataframes and summary.txt inside of hg002_hap[12]/
