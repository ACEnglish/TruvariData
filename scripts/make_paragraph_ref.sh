IN=$1
OUT=$2
REF=$3
TMP=/raid/home/english/science/english/wp1.5/tmpdir/
META=/raid/home/english/science/english/wp1.5/manifest.txt
PAR=/home/english/software/paragraph/bin/multigrmpy.py
mkdir $OUT
zcat $IN | cut -f1-9 | bgzip > $OUT/tmp.vcf.gz
$PAR -i ${OUT}/tmp.vcf.gz \
    -m $META \
    --scratch-dir $TMP \
    -o ${OUT} \
    -r $REF

