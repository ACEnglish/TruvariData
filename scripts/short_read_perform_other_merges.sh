# list holding full paths to each variant
set -e
input_file=$1
reference=$2
# Update these for your paths
survivor=/users/u233287/scratch/insertion_ref/msru/software/SURVIVOR-1.0.6/Debug/SURVIVOR
jasmine=/users/u233287/scratch/misc_software/Jasmine-1.1.4/run.sh
# skipping this
#svimmer=/users/u233287/scratch/insertion_ref/msru/software/svimmer-0.1/svimmer
# See the IMPORTANT note below for svimmer
nproc=1
#keep_chrs="chr1,chr2,chr3,chr4,chr5,chr6,chr7,chr8,chr9,chr10,chr11,chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19,chr20,chr21,chr22,chrX,chrY"
keep_chrs="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,X,Y"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Need to make per-sample SV only VCFs (compressed and not compressed) and put them into a file
mkdir -p vcfs
mkdir -p gzvcfs
echo "Extracting SVs"
cat $input_file | while read vcf
do
    #inter merges
    #samp_name=$(echo $vcf | rev  | cut -f2 -d\/ | rev)
    # manta
    samp_name=$(echo $(basename $vcf) | cut -f1 -d\.)
    # Manta format filtering - also passonly - this also takes out unresolved SVs
    bcftools view -r $keep_chrs $vcf \
        | python $DIR/only_svs.py /dev/stdin passonly \
        | bcftools annotate -x FORMAT/FT,FORMAT/GQ,FORMAT/PL,FORMAT/PR,FORMAT/SR > vcfs/${samp_name}.vcf
    bgzip -c vcfs/${samp_name}.vcf > gzvcfs/${samp_name}.vcf.gz
    tabix -f gzvcfs/${samp_name}.vcf.gz
done
mkdir -p temp/
ls vcfs/*.vcf > temp/plain.txt
ls gzvcfs/*.vcf.gz > temp/plain.gzip.txt

echo "Running survivor"
echo $(date)
$survivor merge temp/plain.txt 1000 1 1 0 1 50 temp/survivor.1000.vcf
echo $(date)
cat temp/survivor.1000.vcf | sed 's/\.\/\./0\/0/g' | vcf-sort | bcftools +fill-tags |  bgzip > survivor.1000.vcf.gz
tabix -f survivor.1000.vcf.gz

echo "Running jasmine"
echo $(date)
$jasmine file_list=temp/plain.txt out_file=jasmine.vcf threads=$nproc --output_genotypes --default_zero_genotype
echo $(date)
$DIR/vcf_compress.sh jasmine.vcf

echo "Running Exact"
echo $(date)
bcftools merge -0 -l temp/plain.gzip.txt -f x -m none | bgzip > exact.vcf.gz
echo $(date)
tabix -f exact.vcf.gz
echo "Running Naive"
echo $(date)
python $DIR/naive_50.py -c temp/ncollap.vcf -i exact.vcf.gz -O .5 -p 0 -o naive.vcf --chain
echo $(date)
$DIR/vcf_compress.sh naive.vcf

echo "Running Truvari"
echo $(date)
truvari collapse --chain --reference ${reference} -i exact.vcf.gz -o truvari.vcf -c temp/collapse.vcf
echo $(date)
$DIR/vcf_compress.sh truvari.vcf

#echo "Building dataframes"
#truvari vcf2df -i exact.vcf.gz exact.jl
#truvari vcf2df -i survivor.1000.vcf.gz survivor.1000.jl
#truvari vcf2df -i jasmine.vcf.gz jasmine.jl
#truvari vcf2df -i naive.vcf.gz naive.jl
#truvari vcf2df -i truvari.vcf.gz truvari.jl
