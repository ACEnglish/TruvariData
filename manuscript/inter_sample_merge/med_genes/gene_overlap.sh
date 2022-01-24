
mkdir -p gene_anno/
truvari anno bpovl -i ../data/grch38/exact.vcf.gz -a Homo_sapiens.GRCh38.105.chr.sorted.gtf.gz -p gff -o gene_anno/exact.jl
truvari anno bpovl -i ../data/grch38/jasmine.vcf.gz -a Homo_sapiens.GRCh38.105.chr.sorted.gtf.gz -p gff -o gene_anno/jasmine.jl
truvari anno bpovl -i ../data/grch38/naive.vcf.gz -a Homo_sapiens.GRCh38.105.chr.sorted.gtf.gz -p gff -o gene_anno/naive.jl
truvari anno bpovl -i ../data/grch38/survivor.vcf.gz -a Homo_sapiens.GRCh38.105.chr.sorted.gtf.gz -p gff -o gene_anno/survivor.jl
truvari anno bpovl -i ../data/grch38/truvari.vcf.gz -a Homo_sapiens.GRCh38.105.chr.sorted.gtf.gz -p gff -o gene_anno/truvari.jl
