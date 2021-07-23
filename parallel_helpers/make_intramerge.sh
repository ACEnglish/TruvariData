declare -A references
references=( ["chm13"]="/users/u233287/scratch/insertion_ref/reference/chm13/chm13.draft_v1.0.fasta"
             ["hg19"]="/users/u233287/scratch/insertion_ref/reference/hg19/hg19.fa"
             ["grch38"]="/users/u233287/scratch/insertion_ref/reference/grch38/GRCh38_1kg_mainchrs.fa"
             ["pr1"]="/users/u233287/scratch/insertion_ref/reference/pr1/PR1.fa.gz"
        )

mkdir -p jobs/logs
find `pwd`/ -name "exact.vcf.gz" | while read in_vcf
do
    ref=$(echo ${in_vcf} | cut -f8 -d/)
    ref="${references[$ref]}"
    jname=$(echo ${in_vcf} | cut -f2- -d\/ | sed 's/\//_/g')
    echo "bash /users/u233287/scratch/insertion_ref/msru/scripts/single_sample_collapse.sh $in_vcf $ref" > jobs/${jname}.sh
done
