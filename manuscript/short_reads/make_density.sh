mkdir -p density/
#truvari anno density -i ../inter_sample_merge/data/grch38/exact.vcf.gz -w 1000 -g genome.bed -m mask.bed    -o density/lr_grch38_exact.jl
#truvari anno density -i ../inter_sample_merge/data/grch38/jasmine.vcf.gz -w 1000 -g genome.bed -m mask.bed  -o density/lr_grch38_jasmine.jl
#truvari anno density -i ../inter_sample_merge/data/grch38/naive.vcf.gz -w 1000 -g genome.bed -m mask.bed    -o density/lr_grch38_naive.jl
#truvari anno density -i ../inter_sample_merge/data/grch38/survivor.vcf.gz -w 1000 -g genome.bed -m mask.bed -o density/lr_grch38_survivor.jl
truvari anno density -i ../inter_sample_merge/data/grch38/truvari.vcf.gz -w 1000 -g genome.bed -m mask.bed  -o density/lr_grch38_truvari.jl

#truvari anno density -i srpvcfs/grch38/exact.vcf.gz -w 1000 -g genome.bed -m mask.bed -o density/sr_grch38_exact.jl
#truvari anno density -i srpvcfs/grch38/jasmine.vcf.gz -w 1000 -g genome.bed -m mask.bed -o density/sr_grch38_jasmine.jl
#truvari anno density -i srpvcfs/grch38/naive.vcf.gz -w 1000 -g genome.bed -m mask.bed -o density/sr_grch38_naive.jl
#truvari anno density -i srpvcfs/grch38/survivor.1000.vcf.gz -w 1000 -g genome.bed -m mask.bed -o density/sr_grch38_survivor.jl
truvari anno density -i srpvcfs/grch38/truvari.vcf.gz -w 1000 -g genome.bed -m mask.bed -o density/sr_grch38_truvari.jl
