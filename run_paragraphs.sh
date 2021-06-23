# Run inside 
# Run this in a reference destination directory / merge strategy (e.g. grch38/exact_merge)
# And provide G as first argument to make the grch38 version, else chm13 is used

export TMPDIR=/raid/home/english/science/english/wp1.5/tmpdir/
export TMP=/raid/home/english/science/english/wp1.5/tmpdir/
export TEMP=/raid/home/english/science/english/wp1.5/tmpdir/
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PARSH=$DIR/make_paragraph_ref.sh
ONLYSV=$DIR/only_svs.py
vcf=$1
reference=$2
outdir=$3

mkdir -p $outdir

python $ONLYSV $vcf | bgzip > ${outdir}/sv_only.vcf.gz
bash $PARSH $outdir/sv_only.vcf.gz ${outdir}/paragraph $reference 


