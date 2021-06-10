# Run this in a reference destination directory / merge strategy (e.g. grch38/exact_merge)
# And provide G as first argument to make the grch38 version, else chm13 is used
# Be sure to update the TMPDIR and reference files
export TMPDIR=/raid/home/english/science/english/wp1.5/tmp/
files=files.txt
header=header.txt
reference=$1
if [ "${1}" == "G" ]
then
    reference=/home/english/science/english/wp1.5/reference/GRCh38_1kg_mainchrs.fa
else
    reference=/home/english/science/english/wp1.5/reference/t2t_CHM13v1/chm13.draft_v1.0.fasta
fi

bcftools merge -l $files -m none -0 --use-header $header \
    | bcftools annotate -x INFO/QNAME,INFO/QSTART,INFO/QSTRAND \
    | bcftools +fill-tags | bgzip > exact.vcf.gz
tabix exact.vcf.gz

truvari collapse --reference $reference \
 	-i exact.vcf.gz \
	-c removed.strict.vcf \
	-o strict.vcf
vcf-sort strict.vcf | bcftools +fill-tags | bgzip > strict.vcf.gz
tabix strict.vcf.gz

truvari collapse --reference $reference \
 	-i exact.vcf.gz \
	-c removed.loose.vcf \
	-o loose.vcf \
	-p 0.7 -P 0.7 -r 1000
vcf-sort loose.vcf | bcftools +fill-tags | bgzip > loose.vcf.gz



