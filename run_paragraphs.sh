# Run inside 
# Run this in a reference destination directory / merge strategy (e.g. grch38/exact_merge)
# And provide G as first argument to make the grch38 version, else chm13 is used

export TMPDIR=/raid/home/english/science/english/wp1.5/tmpdir/
export TMP=/raid/home/english/science/english/wp1.5/tmpdir/
export TEMP=/raid/home/english/science/english/wp1.5/tmpdir/
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PARSH=$DIR/make_paragraph_ref.sh
ONLYSV=$DIR/only_svs.py
reference=$1
if [ "${1}" == "G" ]
then
    reference=/home/english/science/english/wp1.5/reference/GRCh38_1kg_mainchrs.fa
else
    reference=/home/english/science/english/wp1.5/reference/t2t_CHM13v1/chm13.draft_v1.0.fasta
fi

for i in exact.vcf.gz loose.vcf.gz strict.vcf.gz
do
    obase=${i%.vcf.gz}
    oname=${obase}.sv.vcf.gz
    python $ONLYSV $i | bgzip > $oname
    bash $PARSH $oname ${obase}_paragraph $reference &
done
wait
