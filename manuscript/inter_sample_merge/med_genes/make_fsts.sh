
META=~/scratch/insertion_ref/msru/metadata/sample_metadata.txt
SCRIPT=~/scratch/insertion_ref/msru/scripts/calc_fst.py

echo 'exa'
python $SCRIPT vcfs/exa.vcf.gz $META vcfs/exa
echo 'jas'
python $SCRIPT vcfs/jas.vcf.gz $META vcfs/jas
echo 'nav'
python $SCRIPT vcfs/nav.vcf.gz $META vcfs/nav
echo 'sur'
python $SCRIPT vcfs/surv.vcf.gz $META vcfs/sur
echo 'tru'
python $SCRIPT vcfs/truv.vcf.gz $META vcfs/tru
