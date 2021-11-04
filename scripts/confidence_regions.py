"""
Given a set of PAFs, genome files, and an output directory
Generate the bedtools command to calculate genomecov and write to directory
"""
import os
import sys
import copy
from collections import defaultdict

def separate_by_reference(paths_fn):
    """
    For a set of files, separate them by reference
    """
    lookup = defaultdict(list)
    with open(paths_fn, 'r') as fh:
        for i in fh:
            i = i.strip()
            ref = os.path.basename(i).split('_')[0]
            lookup[ref].append(i)
    return lookup

def main():
    # I'm just going to make commands with this instead
    cmd_tmpl = "bedtools genomecov -i <(cut -f6,8,9 {inpaf} "
    #cmd_tmpl += "| awk '{if ($$3 < $$2) print $1 \"\t\" $$3 \"\t\" $$2; else print $$0}' "
    cmd_tmpl += "| bedtools sort) -g {genomefai} -bga > {outputbed}"
    paths_fn = sys.argv[1]
    genome_fn = sys.argv[2]
    out_dir = sys.argv[3]
    genome_lookup = {}
    with open(genome_fn, 'r') as fh:
        for line in fh:
            data = line.strip().split('\t')
            genome_lookup[data[0]] = data[1]
    # Okay, I need to make this parallel and I need to output per-paf
    # Then I can make a second script that consolidates per-paf
    by_ref = separate_by_reference(paths_fn)
    for k, v in by_ref.items():
        if k not in genome_lookup:
            continue
        for paf in v:
            outname = os.path.join(out_dir, os.path.basename(paf) + '.coverage.bed')
            print(cmd_tmpl.format(inpaf=paf, genomefai=genome_lookup[k], outputbed=outname))
    # So then, once I have all the regions, I want to do the genomecov again
    # But only of those regions from the per-haplotype with coverage == 1
    # And then I want to only grab thos regions that have the coverage equal to the input number of files
    # (e.g. for a single sample, I'll want to pull out those with coverage == 2 (two haplotypes)
if __name__ == '__main__':
    main()
