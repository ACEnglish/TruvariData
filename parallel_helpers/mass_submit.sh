for i in jobs/*.sh
do
    bname=$(basename ${i})
    echo qsub -d `pwd`/ -o logs/${bname}.log -e logs/${bname}.log -l nodes=1:ppn=8,mem=32g $i
done
