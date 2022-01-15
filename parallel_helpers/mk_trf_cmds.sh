exe=/users/u233287/scratch/misc_software/trf409.legacylinux64
cnt=0
cat parallel_helpers/vcfs.txt | while read vcf ref bed
do
    tmp=${vcf%.vcf.gz}.tmp.vcf.gz
    output=${vcf%.vcf.gz}.anno2.vcf.gz
    job=jobs/anno2.${cnt}.sh
    echo "vcf-sort ${vcf} | bgzip > ${tmp}" > $job
    echo "tabix ${tmp}" >> $job
    echo "truvari anno trf -i ${tmp} -e ${exe} -s ${bed} -f ${ref} -t 8 | vcf-sort | bgzip > ${output}" >> $job
    cnt=$(expr $cnt + 1)
done
