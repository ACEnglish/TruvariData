# list holding full paths to each variant
input_file=$1
# Update these for your paths
survivor=/users/u233287/scratch/insertion_ref/msru/software/SURVIVOR-1.0.6/Debug/SURVIVOR
jasmine=/users/u233287/scratch/insertion_ref/msru/software/Jasmine/run.sh
svimmer=/users/u233287/scratch/insertion_ref/msru/software/svimmer-0.1/svimmer
# See the IMPORTANT note below for svimmer
nproc=8

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Need to make per-sample SV only VCFs (compressed and not compressed) and put them into a file
mkdir -p vcfs
mkdir -p gzvcfs
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
$survivor merge plain.txt 500 1 1 0 1 50 temp/survivor.500.vcf
cat temp/survivor.500.vcf | sed 's/\.\/\./0\/0/g' | vcf-sort | bcftools +fill-tags |  bgzip > survivor.500.vcf.gz
tabix survivor.500.vcf.gz

$survivor merge plain.txt 1000 1 1 0 1 50 temp/survivor.1000.vcf
cat temp/survivor.1000.vcf | sed 's/\.\/\./0\/0/g' | vcf-sort | bcftools +fill-tags |  bgzip > survivor.1000.vcf.gz
tabix survivor.1000.vcf.gz

$jasmine file_list=plain.txt out_file=jasmine.vcf threads=$nproc
$DIR/vcf_compress jasmine.vcf

# IMPORTANT This need the 'chr' removed when running hg19
python $svimmer --threads 48 plain.gzip.txt \
	$(for i in $(seq 1 22) X Y; do echo -n chr$i " "; done) > svimmer.vcf
$DIR/vcf_compress svimmer.vcf

bcftools merge -l plain.gzip.txt -f x -m none | bgzip > gvcfs/temp.vcf.gz
tabix gvcfs/temp.vcf.gz
python $DIR/naive_50.py -i gzvcfs/temp.vcf.gz -O .5 -p 0 -o naive.vcf --chain
$DIR/vcf_compress.sh naive.vcf

truvari truv2df -i -v survivor.500.vcf.gz survivor.500.jl
truvari truv2df -i -v survivor.1000.vcf.gz survivor.1000.jl
truvari truv2df -i -v jasmine.vcf.gz jasmine.jl
truvari truv2df -i -v svimmer.vcf.gz svimmer.jl
truvari truv2df -i -v naive.vcf naive.jl
