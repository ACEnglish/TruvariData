# Run truvari bench and create a dataframe of all the results

# 1 - Make the reference lookup ready
DATADIR=$1
shift

REFBASE=${DATADIR}/reference
declare -A REFLOOKUP
REFLOOKUP[chm13]=$REFBASE/chm13/chm13.draft_v1.0.fasta
REFLOOKUP[grch38]=$REFBASE/grch38/GRCh38_1kg_mainchrs.fa
REFLOOKUP[hg19]=$REFBASE/hg19/hg19.fa

# 2 - Have the base VCFs ready
BASEVCF=$DATADIR/inter_merge/
#chm13/strict/strict.vcf.gz

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
    truvari bench -b $BASEVCF/${reference}/strict/strict.sv.vcf.gz \
                  -c $i -o $OUTDIR/${reference}_${sample}/ -f ${REFLOOKUP[$reference]} \
                  --bSample $sample --no-ref b &
    while [ $(jobs | wc -l) -ge $(nproc) ]
    do
        sleep 5
    done
done


