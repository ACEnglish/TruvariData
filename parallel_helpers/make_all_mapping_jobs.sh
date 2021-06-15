reference=$2
cat $1 | while read samp_name project hap1 hap2
do
    job_sh=jobs/${samp_name}.${project}.sh
    echo mkdir -p ${project}/${samp_name}/ > ${job_sh}
    echo bash /users/u233287/scratch/insertion_ref/msru/mapping.sh $hap1 ${samp_name}.1 $reference >> ${job_sh}
    echo bash /users/u233287/scratch/insertion_ref/msru/mapping.sh $hap2 ${samp_name}.2 $reference >> ${job_sh}
    echo bash /users/u233287/scratch/insertion_ref/msru/merge.sh ${samp_name}.1.vcf.gz ${samp_name}.2.vcf.gz ${project}/${samp_name}/exact >> ${job_sh}
done
