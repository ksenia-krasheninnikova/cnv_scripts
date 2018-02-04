#!/usr/bin/env python

import subprocess

if __name__ == '__main__':
    paths = '/home/genomerussia/main/analysis/cnv/sv/GR/stats/dev/samples.txt'
    accumulated_file = '/home/genomerussia/main/analysis/cnv/sv/GR/stats/dev/gain.all.genes.bed'
    header = ['CHROM','START','END','GENE','DESCR','TRANSCRIPT']
    subprocess.call('awk \'{print $1\"_\"$2\"_\"$3\"\\t\"$4"\\t\"$5"\\t\"$6}\' '+accumulated_file+' | sort -k 1b,1 > tmp_all_genes', shell=True)
    with open(paths) as f:
        for line in f:
            line = line.strip()
            id = line.split('/')[-2]
            header.append(id)
            subprocess.call('awk \'{print $1\"_\"$2\"_\"$3\"\\t\"$5}\' '+line+' | sort -k 1b,1 > tmp_sample', shell=True)
            subprocess.call('join tmp_all_genes tmp_sample > tmp_target; mv tmp_target tmp_all_genes', shell=True)
    subprocess.call('echo \"'+'\t'.join(header)+'\"', shell=True)
    subprocess.call('cat tmp_all_genes', shell=True)
    subprocess.call('rm tmp_all_genes tmp_sample', shell=True)
