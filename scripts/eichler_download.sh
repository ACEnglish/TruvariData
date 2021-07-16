for i in 20200628_HHU_assembly-results_CCS_v12 \
         20200716_UW_assembly-results_CLR_v12 \
         20200717_HHU_assembly-results_CCS_v12 \
         20200810_HHU_assembly-results_HG00514_v12 \
         20200828_JAX_assembly-results_CLR_v12 \
         20200612_HHU_assembly-results_CLR_v12 
do
    echo $i
    wget -r ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/HGSVC2/release/v1.0/assemblies/$i/assemblies/phased/
done
