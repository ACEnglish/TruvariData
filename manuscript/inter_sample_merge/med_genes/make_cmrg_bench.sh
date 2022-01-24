truvari bench -b HG002_GRCh38_CMRG_SV_v1.00.vcf.gz --includebed HG002_GRCh38_CMRG_SV_v1.00.bed \
	-c ../data/grch38/exact.vcf.gz -f ~/scratch/insertion_ref/msru/data/reference/grch38/GRCh38_1kg_mainchrs.fa \
	-o cmrg_bench/exact_cmrg --cSample NA24385 --no-ref c
truvari vcf2df -i -f -b cmrg_bench/exact_cmrg/ lcmrg_bench/exact_cmrg/data.jl

truvari bench -b HG002_GRCh38_CMRG_SV_v1.00.vcf.gz --includebed HG002_GRCh38_CMRG_SV_v1.00.bed \
	-c ../data/grch38/truvari.vcf.gz -f ~/scratch/insertion_ref/msru/data/reference/grch38/GRCh38_1kg_mainchrs.fa \
	-o cmrg_bench/truvari_cmrg --cSample NA24385 --no-ref c
truvari vcf2df -i -f -b cmrg_bench/truvari_cmrg/ cmrg_bench/truvari_cmrg/data.jl

truvari bench -b HG002_GRCh38_CMRG_SV_v1.00.vcf.gz --includebed HG002_GRCh38_CMRG_SV_v1.00.bed \
	-c ../data/grch38/survivor.vcf.gz  -f ~/scratch/insertion_ref/msru/data/reference/grch38/GRCh38_1kg_mainchrs.fa \
	-o cmrg_bench/survivor_cmrg --cSample NA24385 --no-ref c
truvari vcf2df -i -f -b cmrg_bench/survivor_cmrg/ cmrg_bench/survivor_cmrg/data.jl

truvari bench -b HG002_GRCh38_CMRG_SV_v1.00.vcf.gz --includebed HG002_GRCh38_CMRG_SV_v1.00.bed \
	-c ../data/grch38/jasmine.vcf.gz  -f ~/scratch/insertion_ref/msru/data/reference/grch38/GRCh38_1kg_mainchrs.fa \
	-o cmrg_bench/jasmine_cmrg --cSample NA24385 --no-ref c
truvari vcf2df -i -f -b cmrg_bench/jasmine_cmrg/ cmrg_bench/jasmine_cmrg/data.jl

truvari bench -b HG002_GRCh38_CMRG_SV_v1.00.vcf.gz --includebed HG002_GRCh38_CMRG_SV_v1.00.bed \
	-c ../data/grch38/naive.vcf.gz  -f ~/scratch/insertion_ref/msru/data/reference/grch38/GRCh38_1kg_mainchrs.fa \
	-o cmrg_bench/naive_cmrg --cSample NA24385 --no-ref c
truvari vcf2df -i -f -b cmrg_bench/naive_cmrg/ cmrg_bench/naive_cmrg/data.jl
