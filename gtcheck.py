"""
Report genotype performance statistics
"""
import sys
import math
import logging
import argparse
import itertools

import pysam
import joblib
import truvari
import pandas as pd
from collections import Counter, defaultdict

"""
ToDo -
Create a per-variant table with isCorrect states for each of the genotyping approaches
Add arguments that allow me to specify the comparison/base VCF
parse the sample_name from the comparison VCF so that doesn't have to be specified
"""

def parse_args(args):
    parser = argparse.ArgumentParser(prog="collapse", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-b", "--base", type=str, required=True,
                        help="Base VCF with answer genotypes")
    parser.add_argument("-c", "--comp", type=str, required=True,
                        help="Comparison VCF with predicted genotypes")
    parser.add_argument("-v", "--variant-table", type=str, required=True,
                        help="Variant table joblib file to write")
    parser.add_argument("-s", "--summary-table", type=str, required=True,
                        help="Summary table joblib file to write")
    args = parser.parse_args(args)
    truvari.setup_logging(True)
    return args

def genotyper(totCov, altCov, priors=None):
    """
    Given total coverage and altCoverage, try to calculate how many copies
    of the alt are at the position (ref/het/hom) and a quality score
    returns two lists
    - probabilities of 0, 1, or two copies of the allele at the location
    - phred-scaled quality scores of those probs
    """
    #We have no information.. should give up
    if totCov == 0:
        return None

    # previously had avgCov
    if priors is None:
        priors = [0.05, 0.5, 0.95]

    # if len(priors) != 3: # raise exception?

    def log_choose(n, k):
        """ swap for efficiency if k is more than half of n """
        r = 0.0
        if k * 2 > n:
            k = n - k

        for d in range(1, k + 1):
            r += math.log(n, 10)
            r -= math.log(d, 10)
            n -= 1

        return r

    total = totCov  # refCoverage + altCoverage if avgCov is None else avgCov
    alt = altCov  # int(spot.tags["szCount"])
    non_alt = total - alt

    gtList = []

    comb = log_choose(total, alt)
    for p_alt in priors:
        my_gq = comb + alt * math.log(p_alt, 10) + non_alt * math.log(1 - p_alt, 10)
        val = 10 * (-my_gq/10)
        gtList.append(val)

    return gtList

def parse_comp(fn, sample_name, cheats=False, svtype="ALL"):
    """
    Parse a comparison file to make a lookup
    Comparison means an output from biograph
    Returns a dictionary with variantKey and list of [gtcls, minPL, bayes, extra_info]
    """
    v1 = pysam.VariantFile(fn)
    lookup = {}
    GTS = {0: (0, 0), 1: (0, 1), 2: (1, 1)}

    min_same = 0
    min_diff = 0

    for entry in v1:
        if "SVLEN" not in entry.info or abs(entry.info["SVLEN"]) < 50:
            continue
        #if entry.info["NumNeighbors"] > 1:
        #    continue
        #if entry.samples[sample_name]["DP"] > 80 or entry.samples[sample_name]["DP"] < 10: continue
        if svtype == "INS" and len(entry.ref) > len(entry.alts[0]):
            continue # DELs
        if svtype == "DEL" and len(entry.ref) < len(entry.alts[0]):
            continue # INSs
        
        key = "%s:%d-%d.%s" % (entry.chrom, entry.start, entry.stop, entry.alts[0])
        gt = entry.samples[sample_name]["GT"]
        if gt == (None, None):
            gt = (0, 0)
        gtclassifier = truvari.get_gt(gt).name
        
        lookup[key] = [gtclassifier, None, None, None]

        if cheats:
            bayes = genotyper(min(50, entry.samples[sample_name]["DP"]), entry.samples[sample_name]["AD"][1])
        else:
            bayes = genotyper(entry.samples[sample_name]["DP"], entry.samples[sample_name]["AD"][1])
        if bayes is None:
            lookup[key][2] = truvari.get_gt((0, 0)).name
        else:
            bayes = truvari.get_gt(GTS[bayes.index(min(bayes))]).name
            lookup[key][2] = bayes

        if "PL" in entry.samples[sample_name]:
            minval = entry.samples[sample_name]["PL"]
        else:
            minval = [None]
        minidx = minval.index(min(minval))
        minPL = truvari.get_gt(GTS[minidx]).name
        # Cheat on minPL
        if cheats and minval[0] is not None and minPL == "REF" \
            and entry.samples[sample_name]["AD"][1] > 0 \
            and abs(minval[0] - minval[1]) < 15:
            minPL = "HET"
        lookup[key][1] = minPL
        if truvari.get_gt(gt).name == truvari.get_gt(GTS[minidx]).name:
            min_same += 1
        else:
            min_diff += 1

        lookup[key][3] = (minval, entry.samples[sample_name]["AD"])
    return lookup

def cnt_correct(comp, base):
    """
    Haplotype Split Presence
    """
    if base == "REF":
        if comp == "REF":
            return 2, 0
        if comp == "HET":
            return 1, 1
        return 0, 2
    if base == "HET":
        if comp == "REF":
            return 1, 1
        if comp == "HET":
            return 2, 1
        return 1, 1
    if base == "HOM":
        if comp == "REF":
            return 0, 2
        if comp == "HET":
            return 1, 1
        return 2, 0

def one_correct(comp, base):
    """
    Genotype Concordance
    """
    if comp == base:
        return 1, 0
    return 0, 1

def presence_correct(comp, base):
    """
    Pure Presence/Absence
    """
    if base == "REF" and comp == "REF":
        return 1, 0
    if base != "REF" and comp != "REF":
        return 1, 0
    return 0, 1

def parse_base(fn, sample_name, lookup, compare_method=presence_correct, skip_ref=False, svtype="All"):
    """
    Compare the base answer to the comparison's lookup
    Returns the missing count, a lists of correct/incorrect count per genotyping method
    """
    v2 = pysam.VariantFile(fn)
    correct = [0, 0, 0]
    incorrect = [0, 0, 0]
    missing = 0

    incorrect_pair = Counter()
    for entry in v2:
        if entry.chrom != "chr1": break
        if "SVLEN" not in entry.info or abs(entry.info["SVLEN"]) < 50:
            continue
        if svtype == "INS" and len(entry.ref) > len(entry.alts[0]):
            continue # DELs
        if svtype == "DEL" and len(entry.ref) < len(entry.alts[0]):
            continue # INSs
 
        key = "%s:%d-%d.%s" % (entry.chrom, entry.start, entry.stop, entry.alts[0])
        if key not in lookup:
            missing += 1
            continue
        
        cmp_gt = truvari.get_gt(entry.samples[sample_name]["GT"]).name
        state1 = "None"
        if skip_ref and cmp_gt == "REF":
            continue
        for pos in [0, 1, 2]:
            base = lookup[key][pos]
            m_c, m_i = compare_method(base, cmp_gt)
            correct[pos] += m_c
            incorrect[pos] += m_i

       #print(entry.start, cmp_gt, lookup[key], extra_lookup[key], state1, state2, state3, state4, \
       #      entry.info["SVLEN"], entry.info["SVTYPE"])
    return missing, correct, incorrect

if __name__ == '__main__':
    #f2 = "data/other_merges/grch38/nomicro_nosimple/truvari.vcf.gz"
    #f1 = "/home/english/science/english/msru/data/genotyping/biograph/HG00096/HG00096.bg/analysis/grch38.chr1.results.vcf.gz"
    #f1 = "data/genotyping/biograph/HG01114//HG01114.bg/analysis/grch38.chr1.results.vcf.gz"
    #f2 = "/home/english/science/english/msru/data/rob_references/grch38.strict.strict.vcf.gz"
    #f1 = "/home/english/science/english/msru/data/genotyping/grch38.chr1.results.vcf.gz"
    args = parse_args(sys.argv[1:])
    v = pysam.VariantFile(args.comp)
    sample_name = v.header.samples[0]
    logging.info(f"Analyzing sample {sample_name}")
    
    summary_rows = []
    for cmp_method, cmp_name in [(one_correct, "exact"), (presence_correct, "presence"), (cnt_correct, "semi")]:
        for svtype in ["All", "DEL", "INS"]:
            for with_ref in [True, False]:
                for cheats in [False, True]:
                    lookup = parse_comp(args.comp, sample_name, cheats=cheats, svtype=svtype)
                    results = parse_base(args.base, sample_name, lookup, compare_method=cmp_method, \
                                        skip_ref=with_ref, svtype=svtype)
                    summary_rows.append([cmp_name, svtype, with_ref, cheats, results[0], *results[1], *results[2]])
    logging.info("Building DataFrame")
    frame  = pd.DataFrame(summary_rows, columns=["cmp_method", "svtype", "skip_ref", "cheats", "missing", \
                                                 "gtclsCorrect", "minPLCorrect", "bayesCorrect", \
                                                 "gtclsIncorrect", "minPLIncorrect", "bayesIncorrect"])
    joblib.dump(frame, args.summary_table)
    logging.info("Finished")


