# input vcf
# input centromeres and segdups
# parameter for distance 5Mb

#grch38.centromeres.ucsc.bed.gz
#grch38.segdups.ucsc.bed.gz

import pysam
intervaltree?
for entry in pysam:
    entry = centromere(entry, whatever)
    entry = segdup(entry, whatever)
    out.write(entry)

