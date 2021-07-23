hap1=$1
hap2=$2
sample=$3
output=$4

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
bcftools merge --force-samples -m none ${hap1} ${hap2} \
        | python ${DIR}/resolve_gt.py ${sample} \
        | python ${DIR}/annotate_svs.py /dev/stdin \
        | bgzip > ${output}
tabix ${output}
