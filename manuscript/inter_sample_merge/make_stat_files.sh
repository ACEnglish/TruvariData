
# Get all SV counts
find data/ -name  "*.gz" | while read i
do
    echo $i
    bcftools query -f "%INFO/SVTYPE\n" $i | sort| uniq -c 
done > SVCount.txt #| python count_to_table.py

# All AFs
find data -name "*.vcf.gz" | while read i;
do
    echo $i
    bcftools query -f "%INFO/AF\n" $i | awk '{tot += $1; cnt += 1} END {print tot / cnt}'
    bcftools query -i "SVTYPE=='DEL'" -f "%INFO/AF\n" $i | awk '{tot += $1; cnt += 1} END {print tot / cnt}'
    bcftools query -i "SVTYPE=='INS'" -f "%INFO/AF\n" $i | awk '{tot += $1; cnt += 1} END {print tot / cnt}'
done > AllAF.txt

# RepeatMasker Allele Counting
#bcftools query -f "%INFO/NeighId\t%INFO/RM_score\t%INFO/RM_clsfam\n"  data/grch38/exact.vcf.gz > data/grch38/repeatmasker_exact.txt

#python counts_to_table.py SVCount.txt AllAF.txt table_counts.txt


