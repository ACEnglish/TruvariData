# ${reference}/${project}_${strategy}/

mkdir -p jobs
mkdir -p logs

# Need both references

cat single_sample.txt | while read vcf_path reference project sample
do
    jname=${reference}_${project}_${sample}
    mkdir -p ${reference}/${project}_strict
    mkdir -p ${reference}/${project}_loose
    echo truvari collapse --reference  > jobs/${jname}_strict.sh
    echo truvari collapse loose > jobs/${jname}_loose.sh

done
# submit all the jobs
