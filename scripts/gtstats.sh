# Subset the VCFs to only SVs and annotate with NumNeighbors
# Turn the VCFs into dataframes using truv2df
# post_processing step joins the two frames, does the modifications (e.g. truvari.get_gt) 
#   and do the three comparison approaches
# Save this output as a new dataframe that can be parsed efficiently by a notebook.
# Eventually I'll join multiple Stats frames to do the full-scale analysis

in_base_vcf=$1
in_comp_vcf=$2
sample_name=$3
destination=$4

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
UNIQTMP=${sample_name}.jl
vcf-subset -c $sample_name $in_base_vcf \
    | python $DIR/only_svs.py /dev/stdin  \
    | truvari anno numneigh \
    | truvari truv2df -i -f -v /dev/stdin base_$UNIQTMP &
python $DIR/only_svs.py $in_comp_vcf \
    | truvari anno numneigh \
    | truvari truv2df -i -f -v /dev/stdin comp_$UNIQTMP &
wait
#python $DIR/gtcheck.py base_$UNIQTMP comp_$UNIQTMP $destination
