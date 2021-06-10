mkdir -p stats
find chm13/ -name "*.vcf.gz" | grep -v removed  | grep -v ".sv." | grep -v paragraph > vcf.files.txt
find grch38/ -name "*.vcf.gz" | grep -v removed  | grep -v ".sv." | grep -v paragraph >> vcf.files.txt
cat vcf.files.txt | while read vcf_file
do
    name=$(echo $vcf_file | sed 's/\//_/g')
    name=${name%.vcf.gz}
    echo "python only_svs.py $i | truvari truv2df -v -f /dev/stdin stats/${name}.jl"
done

for i in $(ls */*loose/*.vcf.gz */*strict/*.vcf.gz | grep -v removed)
do
    name=$(echo $i | sed 's/\//_/g')
    name=${name%.vcf.gz}
    python only_svs.py $i | truvari truv2df -v -f /dev/stdin stats/${name}.jl &
    while [ $( jobs | wc -l ) -ge 35 ]
    do
		sleep 5
    done
done
    
#for i in */*.sv.vcf.gz;
#do
    #name=$(echo $i | sed 's/\//_/g')
    #name=${name%.sv.vcf.gz}
    #IFS='_' read -a array <<< $name 
    #ref=${array[0]}
    #merge=${array[1]}
    #truvari truv2df -v -f $i stats/${ref}_merged_${merge}.jl &
#done
#wait
