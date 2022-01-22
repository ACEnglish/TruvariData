Needs the inter-merge VCFs created as well as other-merges.

Organize them inside data/<reference>/<program>.vcf.gz

Make sure annotations are on them
truvari anno trf
truvari anno Repmask
truvari anno bpovl [tbd]
bcftools +fill-tags

I'm just going to keep these as the final versions. The other directories are temporary working dirs that I can just
remove

1) BCFtools maximum
find data/ -name  "exact.vcf.gz" | while read i; do echo $i; bcftools query -f "%INFO/SVTYPE\n" $i | sort| uniq -c ;
done

data/hg19/exact.vcf.gz
  78057 DEL
 261834 INS
data/grch38/exact.vcf.gz
  80365 DEL
 266836 INS
data/chm13/exact.vcf.gz
 121038 DEL
 208899 INS

# All AFS
find data -name "*.vcf.gz" | while read i;
do
echo $i
 bcftools query -f "%INFO/AF\n" $i | awk '{tot += $1; cnt += 1} END {print tot / cnt}'
 done

 data/hg19/exact.vcf.gz
 tput bel
 0.048182
 data/hg19/hg19.sv.vcf.gz
 0.084581
 data/grch38/exact.vcf.gz
 0.0480493
 data/grch38/truvari.vcf.gz
 0.0840406
 data/grch38/jasmine.vcf.gz
 0.128555
 data/grch38/survivor.vcf.gz
 0.185539
 data/grch38/naive.vcf.gz
 0.137607
 data/chm13/exact.vcf.gz
 0.0446031
 data/chm13/truvari.vcf.gz
 0.0682259
 data/chm13/jasmine.vcf.gz
 0.128532
 data/chm13/survivor.vcf.gz
 0.14068
 data/chm13/naive.vcf.gz
 0.0994234
