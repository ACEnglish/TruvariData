import sys
import joblib
import pandas as pd
import truvari
import gtfparse

meta = [('BCFtools', "../data/grch38/exact.vcf.gz", "gene_anno/exact.jl"),
        ('Jasmine', "../data/grch38/jasmine.vcf.gz", "gene_anno/jasmine.jl"),
        ('Naive', "../data/grch38/naive.vcf.gz", "gene_anno/naive.jl"),
        ('SURVIVOR', "../data/grch38/survivor.vcf.gz", "gene_anno/survivor.jl"),
        ('Truvari', "../data/grch38/truvari.vcf.gz", "gene_anno/truvari.jl")
       ]
parts = []

anno = joblib.load("ensmbl.genes.jl")
view_annos = anno[anno['feature'] == 'gene']

for name, vcf_fn, vcf_anno_fn in meta:
    vcf = truvari.vcf_to_df(vcf_fn, with_info="True")
    vcf_anno = joblib.load(vcf_anno_fn)

    vcf['AF'] = vcf['AF'].apply(lambda x: x[0])
    # Subset annotation to only certain types of hits
    view_vcf_anno = vcf_anno[vcf_anno['anno_key'].isin(view_annos.index)]

    # subset the vcf to only hits
    hits = vcf.loc[view_vcf_anno['vcf_key'].unique()]

    # Then pull out the SVTYPE and AF and Count
    cnts = hits.groupby(['svtype']).size().to_frame('count')
    afs = hits.groupby(['svtype'])['AF'].mean()

    out = cnts.join(afs).loc[["DEL", "INS"]].reset_index()
    out['merge'] = name
    parts.append(out)

parts = pd.concat(parts)
parts.to_csv('merge_gene_hits.txt', sep='\t', index=False)
