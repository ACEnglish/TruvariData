base_vcf=$1
comp_vcf=$2
reference=$3
sample=$4
outdir=$5

truvari bench -b $base_vcf -c $comp_vcf -f $reference \
    --passonly --no-ref a --bSample $sample --cSample $sample \
    -o $outdir/$sample/

truvari vcf2df -i -s $sample -b $outdir/$sample/ $outdir/$sample/data.jl

for i in $outdir/$sample/*.vcf
do
    vcf_compress $i
done
