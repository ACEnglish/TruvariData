for i in jobs/*.sh; do qsub -A proj-dm0022 -d `pwd`/ -o logs/$(basename $i).log -e logs/$(basename $i).log -l nodes=1:ppn=2,mem=8g $i; done
