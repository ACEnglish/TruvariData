sample_name=$1
in_base_vcf=/home/english/science/english/msru/data/rob_references/grch38.strict.strict.vcf.gz
DIR=/home/english/science/english/msru/
python $DIR/only_svs.py $in_base_vcf \
    | vcf-subset -c $sample_name \
    | truvari anno numneigh \
    | truvari truv2df -i -f -v /dev/stdin ${sample_name}.2.base.jl 
