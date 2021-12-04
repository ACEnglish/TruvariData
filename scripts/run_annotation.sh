RMEXE=/users/u233287/scratch/misc_software/RepeatMasker/RepeatMasker
input=$1
reference=$2
output=${input%.vcf.gz}.annotated.vcf.gz
truvari anno repmask -i ${input} -e $RMEXE -T 8 \
    | truvari anno remap -r ${reference} \
    | vcf-sort \
    | truvari anno numneigh \
    | bgzip > ${output}
tabix ${output}
