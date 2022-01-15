# list holding full paths to each variant
set -e
input_file=$1
# Update these for your paths
survivor=/users/u233287/scratch/insertion_ref/msru/software/SURVIVOR-1.0.6/Debug/SURVIVOR
jasmine=/users/u233287/scratch/misc_software/Jasmine-1.1.4/run.sh
# skipping this
#svimmer=/users/u233287/scratch/insertion_ref/msru/software/svimmer-0.1/svimmer
# See the IMPORTANT note below for svimmer
nproc=8

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Need to make per-sample SV only VCFs (compressed and not compressed) and put them into a file
mkdir -p vcfs
mkdir -p gzvcfs
echo "Extracting SVs"
cat $input_file | while read vcf
do
    samp_name=$(echo $vcf | rev  | cut -f2 -d\/ | rev)
    python $DIR/only_svs.py $vcf > vcfs/${samp_name}.vcf
    bgzip -c vcfs/${samp_name}.vcf > gzvcfs/${samp_name}.vcf.gz
    tabix gzvcfs/${samp_name}.vcf.gz
done
ls vcfs/*.vcf > plain.txt
ls gzvcfs/*.vcf.gz > plain.gzip.txt

mkdir -p temp/
echo "Running survivor"
$survivor merge plain.txt 500 1 1 0 1 50 temp/survivor.500.vcf
cat temp/survivor.500.vcf | sed 's/\.\/\./0\/0/g' | vcf-sort | bcftools +fill-tags |  bgzip > survivor.500.vcf.gz
tabix survivor.500.vcf.gz

$survivor merge plain.txt 1000 1 1 0 1 50 temp/survivor.1000.vcf
cat temp/survivor.1000.vcf | sed 's/\.\/\./0\/0/g' | vcf-sort | bcftools +fill-tags |  bgzip > survivor.1000.vcf.gz
tabix survivor.1000.vcf.gz

echo "Running jasmine"
$jasmine file_list=plain.txt out_file=jasmine.vcf threads=$nproc --output_genotypes --default_zero_genotype
$DIR/vcf_compress.sh jasmine.vcf

echo "Running Naive"
bcftools merge -0 -l plain.gzip.txt -f x -m none | bgzip > gzvcfs/temp.vcf.gz
tabix gzvcfs/temp.vcf.gz
python $DIR/naive_50.py -i gzvcfs/temp.vcf.gz -O .5 -p 0 -o naive.vcf --chain
$DIR/vcf_compress.sh naive.vcf

echo "Building dataframes"
truvari vcf2df -i survivor.500.vcf.gz survivor.500.jl
truvari vcf2df -i survivor.1000.vcf.gz survivor.1000.jl
truvari vcf2df -i jasmine.vcf.gz jasmine.jl
truvari vcf2df -i naive.vcf.gz naive.jl

#echo "Running svimmer <-- the release didn't work. It would hang"
# IMPORTANT This need the 'chr' removed when running different references
#GRCH38_CHRS=$(for i in $(seq 1 22) X Y; do echo -n chr$i " "; done)
#CHM13_CHRS=$(for i in $(seq 1 22) X; do echo -n chr$i " "; done)
#HG19_CHRS=$(for i in $(seq 1 22) X Y; do echo -n $i " "; done)
#echo $CHRS
#python $svimmer plain.gzip.txt $CHM13_CHRS > svimmer.vcf
#$DIR/vcf_compress.sh svimmer.vcf
#truvari truv2df -i -v svimmer.vcf.gz svimmer.jl
