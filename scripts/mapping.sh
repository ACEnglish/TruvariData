# Input fasta haplotype
fasta=$1
# Sample name for the output vcf
name=$2
# Reference
ref=$3
aln_name=$(basename $fasta)
minimap2 -cx asm5 -t8 -k20 --secondary=no --cs ${ref} ${fasta} | sort -k6,6 -k8,8n > ${aln_name}.paf
paftools.jl stat ${aln_name}.paf
cat ${aln_name}.paf | paftools.js call -f ${ref} -L10000 - | vcf-sort | bgzip > ${name}.vcf.gz
tabix ${name}.vcf.gz
