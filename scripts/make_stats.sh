vcf_file=$1

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
out_name=${vcf_file%.vcf.gz}.jl

python $DIR/only_svs.py $vcf_file | truvari vcf2df -i -f /dev/stdin $out_name

