
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("regioneR")

library(regioneR)

genome <- toGRanges("short_read/GRCh38_1kg_mainchrs.fa.fai")
my.regions <- toGRanges("short_read/Missing1k.txt", genome=genome)
all.trf <- toGRanges("short_read/grch38.simpleRepeat.bed", genome=genome)
my.mask <- toGRanges("short_read/grch38.exclude_regions.bed", genome=genome)

length(my.regions)
length(all.trf)
length(my.mask)


pt <- permTest(A=my.regions, B=all.trf, randomize.function=randomizeRegions,
               evaluate.function=numOverlaps, genome=genome)
