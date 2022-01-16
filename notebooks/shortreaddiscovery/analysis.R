# use docker to setup R easily
# docker run --rm -p 8787:8787 --cpus=4 -e PASSWORD=yourpasswordhere rocker/rstudio

# Update container with required libraries
# docker exec -it <container_name> /bin/bash
# apt-get -qq update && apt-get install -yq libxml2 liblzma-dev libbz2-dev libz-dev

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

pt <- permTest(A=my.regions, B=all.trf, ntimes=1000, randomize.function=randomizeRegions,
               evaluate.function=numOverlaps, genome=genome, mask=my.mask)
