
in_vcf=$1
region=/users/u233287/scratch/insertion_ref/msru/data/other_merges/grch38/med_genes/GRCh38_CMRG_benchmark_gene_coordinates.bed
declare -A samps
samps[AMR]="HG01114,HG00731,NA19650,HG00732,HG00733"
samps[EUR]="NA12878,HG01505,HG00096,HG00171,NA20509,NA12329,NA24385,PGP1"
samps[AFR]="HG02011,NA19983,NA19239,HG02587,HG03486,HG03065,HG02818,HG03371,HG03125,NA19240,NA19238"
samps[SAS]="HG03009,NA20847,HG03732,HG02492,HG03683"
samps[EAS]="HG01596,HG00513,HG00512,NA18534,HG00864,HG00514,NA18939"


function calculate()
{
    anc=$1
    echo $anc 
    s=${samps[$anc]}
    bcftools view -s $s -R $region $in_vcf | bcftools +fill-tags \
        | bcftools query -f "%INFO/MAF\n" | awk '{tot += $1; cnt += 1} END {print tot / cnt}'
    bcftools view -i 'SVTYPE == "DEL"' -s $s -R $region $in_vcf | bcftools +fill-tags \
        | bcftools query -f "%INFO/MAF\n" | awk '{tot += $1; cnt += 1} END {print tot / cnt}'
    bcftools view -i 'SVTYPE == "INS"' -s $s -R $region $in_vcf | bcftools +fill-tags \
        | bcftools query -f "%INFO/MAF\n" | awk '{tot += $1; cnt += 1} END {print tot / cnt}'
}

calculate "AMR"
calculate "EUR"
calculate "AFR"
calculate "SAS"
calculate "EAS"
