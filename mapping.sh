
#ref=/users/u233287/scratch/insertion_ref/reference/GRCh38_1kg_mainchrs.fa
#ref=/users/u233287/scratch/insertion_ref/reference/t2t_CHM13v1/chm13.draft_v1.0.fasta
# Input fasta haplotype
fasta=$1
name=$2
ref=$3
aln_name=$(basename $fasta)
minimap2 -cx asm5 -t8 --cs ${ref} ${fasta} | sort -k6,6 -k8,8n > ${aln_name}.paf
cat ${aln_name}.paf | paftools.js call -f ${ref} -L10000 - | vcf-sort | bgzip > ${name}.var.vcf.gz
tabix ${name}.var.vcf.gz


