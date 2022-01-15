bcftools query -f "%CHROM\t%POS\t%INFO/NeighId\t%INFO/SVLEN\t%INFO/SVTYPE\t%INFO/TRFcopies\t%INFO/TRFDiff\t%INFO/TRFrepeat\t%ALT\n" \
    -i "TRF == 1" $1 | sort -k3,3V -k7,7n
