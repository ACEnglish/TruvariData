# Run truvari bench and create a dataframe of all the results
# Manually include/remove --includebed argument
# Args:
# 1  - Full directory of the msru/data
# 2  - Output directory
# 3+ - VCF(s) to process
DATADIR=$1
shift

# 1 - Make the reference lookup ready
REFBASE=${DATADIR}/reference
declare -A REFLOOKUP
REFLOOKUP[chm13]=$REFBASE/chm13/chm13.draft_v1.0.fasta
REFLOOKUP[grch38]=$REFBASE/grch38/GRCh38_1kg_mainchrs.fa
REFLOOKUP[hg19]=$REFBASE/hg19/hg19.fa

declare -A BEDLOOKUP
BEDLOOKUP[chm13]=$DATADIR/genes/chm13.merged.gencode35.bed
BEDLOOKUP[grch38]=$DATADIR/genes/grch38.merged.gencode35.bed
BEDLOOKUP[hg19]=$DATADIR/genes/hg19.merged.gencode35.bed

# 2 - Have the base VCFs ready
BASEVCF=$DATADIR/inter_merge/

# 3 - Set the output directory
OUTDIR=$1
shift
mkdir -p $OUTDIR

# 4 - Give a bunch of VCFs to process. Expecting sample.reference.vcf.gz
for i in "$@"
do
    name=$(basename $i)
    sample=$(echo $name | cut -f1 -d\.)
    reference=$(echo $name | cut -f2 -d\.)
    echo "ref: " $reference " " ${REFLOOKUP[$reference]} " samp: " $sample
    truvari bench -b $BASEVCF/${reference}/strict/strict.anno.sv.vcf.gz \
                  -c $i -o $OUTDIR/${reference}_${sample}/ -f ${REFLOOKUP[$reference]} \
                  --bSample $sample --no-ref b --passonly & #--includebed ${BEDLOOKUP[$reference]} &
    while [ $(jobs | wc -l) -ge $(nproc) ]
    do
        sleep 5
    done
done
wait
