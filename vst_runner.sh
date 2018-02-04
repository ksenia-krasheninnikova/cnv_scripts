#!/bin/bash

path_script='/home/genomerussia/tools/cnv_scripts/bin/count_Vst.py'
sizes='/home/genomerussia/tools/cnv_scripts/reference/hg38.size'
chrom=$1
first_pop_path=$2
second_pop_path=$3
destination=$4
echo ${chrom} ${first_pop_path} ${second_pop_path} ${destination}
${path_script} --sizes ${sizes} --chrom chr${chrom} --window 100000 ${first_pop_path} ${second_pop_path} ${destination}.chr${chrom}.100K.txt
