TMPDIR=/home/english/science/english/wp1.5/tmp/
GRCHFA=/home/english/science/english/wp1.5/reference/GRCh38_1kg_mainchrs.fa
CHM13FA=/home/english/science/english/wp1.5/reference/t2t_CHM13v1/chm13.draft_v1.0.fasta

cat single_sample.txt | while read vcf_path
do

    IFS='/' read -a array <<< $vcf_path

    reference=${array[0]}
    project=${array[1]}
    sample=$(echo ${array[2]%.vcf.gz} | cut -f1 -d\_)

    if [ $reference == "grch38" ]
    then
        reference_path=$GRCHFA
    else
        reference_path=$CHM13FA
    fi
    mkdir -p ${reference}/${project}_strict/
    mkdir -p ${reference}/${project}_loose/
    truvari collapse --hap --reference $reference_path \
        -i $vcf_path \
        -c ${reference}/${project}_strict/removed.${sample}.vcf \
        -o ${reference}/${project}_strict/${sample}.vcf 2> logs/${reference}_${project}_${loose}_strict.log &

    truvari collapse --hap --reference $reference_path \
        -i $vcf_path \
        -c ${reference}/${project}_loose/removed.${sample}.vcf \
        -o ${reference}/${project}_loose/${sample}.vcf \
        -p 0.7 -P 0.7 -r 1000 2> logs/${reference}_${project}_${sample}_loose.log &
    while [ $( jobs | wc -l ) -ge 35 ]
	do
		sleep 5
	done
done

wait


