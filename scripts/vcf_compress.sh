function cleanup() { 
    fn=$1;
    vcf-sort -t `pwd`/ ${fn} | bgzip > ${fn}_tmp.vcf.gz
    mv ${fn}_tmp.vcf.gz ${fn}.gz
    tabix ${fn}.gz
    rm -rf ${fn}
}

cleanup $1
