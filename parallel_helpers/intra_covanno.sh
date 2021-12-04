find data/inter_merge/ -name *"vcf.gz" | grep -v removed | grep -v pr1 | while read line; do echo "python
scripts/hc_region_annotate.py $line data/coverage_beds/$(echo $line | cut -f3 -d/).single_coverage.bed | bgzip >
${line%.vcf.gz}.covanno.vcf.gz"; done | parallel -j $(nproc)
