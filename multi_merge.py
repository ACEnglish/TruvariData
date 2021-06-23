"""
Given a directory full of single-sample merges on the same reference

Group all of the same-strategy merges and then do exact/strict/loose for each

Then provide an output directory and a reference. 

Warning - the output directory should not be the same as the input directory

Find all of the same-strategy single-sample merges (exact strict merge)

For each of the same type sets, do an exact, strict, and loose merge

So we'll output in a single directory (e.g. merges/reference_name)
And then we'll do bcftools merge truvari twice
"""
import os
import sys
import glob
import tempfile
from pathlib import Path
from acebinf import cmd_exe


def get_paths(in_dir, pattern):
    ret = []
    for _ in Path(in_dir).rglob(pattern):
        _ = str(_)
        if "removed" not in _:
            ret.append(_)
    return ret

def make_exact_merge_cmds(in_files, out_dir):
    """
    """
    files = " ".join(in_files)
    samples = []
    for i in in_files:
        # hard assumption
        samples.append(i.split('/')[-2])
    samples = "\t".join(samples)
    header = tempfile.NamedTemporaryFile()
    # make a temporary file of the header
    header_cmd = f"bcftools merge -m none -0 --force-samples --print-header {files} > {header.name}"
    ret = cmd_exe(header_cmd)
    new_header_fn = header.name + "altered"
    new_header = open(new_header_fn, 'w')
    with open(header.name, 'r') as fh:
        for line in fh:
            if line.startswith("##"):
                new_header.write(line)
            else:
                new_header.write(f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{samples}\n")

    # Why do I need the header and file names... right, because of the friggin lack of sample names
    exact_cmd = f"bcftools merge -m none -0 --use-header {new_header_fn} {files}"
    exact_cmd += "| bcftools annotate -x INFO/QNAME,INFO/QSTART,INFO/QSTRAND "
    exact_cmd += f"| bcftools +fill-tags | bgzip > {out_dir}/exact.vcf.gz\n"
    exact_cmd += f"tabix {out_dir}/exact.vcf.gz"
    return exact_cmd

def make_collapse_cmds(out_dir, reference):
    """
    """
    base_cmd = f"truvari collapse --reference {reference} -i {out_dir}/exact.vcf.gz "

    strict_cmd = base_cmd + f"-c {out_dir}/removed.strict.vcf -o {out_dir}/strict.vcf\n"
    strict_cmd += f"vcf-sort {out_dir}/strict.vcf | bcftools +fill-tags | bgzip > {out_dir}/strict.vcf.gz\n"
    strict_cmd += f"tabix {out_dir}/strict.vcf.gz"

    loose_cmd = base_cmd + f"-p 0.7 -P 0.7 -r 1000 -c {out_dir}/removed.loose.vcf -o {out_dir}/loose.vcf\n"
    loose_cmd += f"vcf-sort {out_dir}/loose.vcf | bcftools +fill-tags | bgzip > {out_dir}/loose.vcf.gz\n"
    loose_cmd += f"tabix {out_dir}/loose.vcf.gz"
    
    return strict_cmd, loose_cmd


if __name__ == '__main__':
    in_dir, out_dir, reference = sys.argv[1:]
    exact = get_paths(in_dir, "*exact.vcf.gz")
    strict = get_paths(in_dir, "*strict.vcf.gz")
    loose = get_paths(in_dir, "*loose.vcf.gz")
    for name, files in [("exact", exact), ("strict", strict), ("loose", loose)]:
        dest = os.path.join(out_dir, name)
        print(f'mkdir -p {dest}')
        exact_cmd = make_exact_merge_cmds(files, dest)
        collapse_cmds = make_collapse_cmds(dest, reference)
        print("\n#exact")
        print(exact_cmd)
        print("\n#strict")
        print(collapse_cmds[0])
        print("\n#loose")
        print(collapse_cmds[1])
