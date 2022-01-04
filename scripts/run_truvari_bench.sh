# Run truvari bench and create a dataframe of all the results
# Manually include/remove --includebed argument
# Args:
# 1  - Full directory of the msru/data
# 2  - Output directory
# 3+ - VCF(s) to process
NPROC=8
DATADIR=$1
shift

# 1 - Make the lookups
REFBASE=${DATADIR}/reference
declare -A REFLOOKUP
REFLOOKUP[chm13]=$REFBASE/chm13/chm13.draft_v1.0.fasta
REFLOOKUP[grch38]=$REFBASE/grch38/GRCh38_1kg_mainchrs.fa
REFLOOKUP[sv]=$REFBASE/grch38/GRCh38_1kg_mainchrs.fa
REFLOOKUP[hg19]=$REFBASE/hg19/hg19.fa

declare -A BEDLOOKUP
BEDLOOKUP[chm13]=$DATADIR/genes/chm13.merged.gencode35.bed
BEDLOOKUP[grch38]=$DATADIR/genes/grch38.merged.gencode35.bed
BEDLOOKUP[sv]=$DATADIR/genes/grch38.merged.gencode35.bed
BEDLOOKUP[hg19]=$DATADIR/genes/hg19.merged.gencode35.bed

# 2 - Have the base VCFs ready
declare -A BASEVCF
BASEVCF[chm13]=$DATADIR/inter_merge/final/chm13.sv.vcf.gz
BASEVCF[grch38]=$DATADIR/inter_merge/final/grch38.sv.vcf.gz
BASEVCF[sv]=$DATADIR/inter_merge/final/grch38.sv.vcf.gz
BASEVCF[hg19]=$DATADIR/inter_merge/final/hg19.sv.vcf.gz

# 3 - Set the output directory
OUTDIR=$1
shift
mkdir -p $OUTDIR

# 4 - Give a bunch of input VCFs to process
for i in "$@"
do
    name=$(basename $i)
    sample=$(echo $name | cut -f1 -d\.)
    reference=$(echo $name | cut -f2 -d\.)
    echo "ref: " $reference " " ${REFLOOKUP[$reference]} " samp: " $sample
    truvari bench -b ${BASEVCF[$reference]} \
                  -c $i -o $OUTDIR/${reference}_${sample}/ -f ${REFLOOKUP[$reference]} \
                  --bSample $sample --no-ref b --passonly & #--includebed ${BEDLOOKUP[$reference]} &
    while [ $(jobs | wc -l) -ge ${NPROC} ]
    do
        sleep 5
    done
done
wait
