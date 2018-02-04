#!/bin/bash

prefix='/home/genomerussia/main/analysis/cnv/sv/GR/'

for path in ${prefix}/GR* 
do
    id=$(basename ${path})
    echo $id
    #./filter_deviated_cnvs.py ${path}/result.copynumber.cw_norm.noXY.bed > ${path}/${id}.deviated.bed 
    cat ${path}/${id}.deviated.bed | grep 'upper' > ${path}/${id}.deviated.gain.bed
    cat ${path}/${id}.deviated.bed | grep 'lower' > ${path}/${id}.deviated.loss.bed
    rm ${path}/${id}.deviated.lower.bed
done 
