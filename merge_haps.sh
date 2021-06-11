hap1=$1
hap2=$2
sample=$3

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
bcftools merge --force-samples -m none ${hap1} ${hap2} \
        | python ${DIR}/resolve_gt.py \
        | bgzip > ${sample}.vcf.gz
tabix ${sample}.vcf.gz
