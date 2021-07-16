set -e

vcf_path=$1
reference=$2
destination=$(dirname $vcf_path)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

truvari collapse --hap --reference $reference \
    -i $vcf_path \
    -o ${destination}/strict.vcf \
    -c ${destination}/removed.strict.vcf 2> ${destination}/collapse.strict.log &
    
truvari collapse --hap --reference $reference \
    -i $vcf_path \
    -o ${destination}/loose.vcf \
    -c ${destination}/removed.loose.vcf  \
    -p 0.7 -P 0.7 -r 1000 2> $destination/collapse.loose.log &
    
wait

for i in ${destination}/*.vcf
do
    bash $DIR/vcf_compress.sh $i
done
