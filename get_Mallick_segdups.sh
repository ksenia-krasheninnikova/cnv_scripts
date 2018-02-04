#!/bin/bash

prefix=/mnt/sochi/ksenia/mallick/cnv/sv/
s=$1
cat $prefix/$s/$s.depth.cw_norm.bed | grep -v 'chrX' | grep -v 'chrY' >  $prefix/$s/$s.depth.cw_norm.noXY.bed && cat $prefix/$s/result.copynumber.bed | grep -v 'chrX' | grep -v 'chrY' > $prefix/$s/result.copynumber.noXY.bed && cut -f5,6 $prefix/$s/$s.depth.cw_norm.noXY.bed| paste $prefix/$s/result.copynumber.noXY.bed /dev/stdin > $prefix/$s/$s.copynumber.cw_norm.noXY.bed && /home/genomerussia/tools/cnv_scripts/bin/find_segdups.py $prefix/$s/$s.copynumber.cw_norm.noXY.bed  > $prefix/$s/$s.copynumber.cw_norm.noXY.seg_dup.bed
