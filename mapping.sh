
# Input fasta haplotype
fasta=$1
name=$2
ref=$3
aln_name=$(basename $fasta)
minimap2 -cx asm5 -t8 --cs ${ref} ${fasta} | sort -k6,6 -k8,8n > ${aln_name}.paf
cat ${aln_name}.paf | paftools.js call -f ${ref} -L10000 - | vcf-sort | bgzip > ${name}.var.vcf.gz
tabix ${name}.var.vcf.gz


