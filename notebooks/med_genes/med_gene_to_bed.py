import pandas as pd

med_genes = pd.read_csv("MRG_medgenes_names.txt")
all_genes = pd.read_csv("grch38.knownGene.txt.gz", sep='\t')

