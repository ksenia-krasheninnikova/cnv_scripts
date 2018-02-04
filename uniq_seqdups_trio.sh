#!/bin/bash

GR='/home/genomerussia/main/analysis/cnv/sv/GR/'

#Overlap segdups
#for town in 'novgorod' 'pskov' 'yakutsk'; do
#    echo 'scanning' ${town}
#    K=''
#    while read id; do
#        K="$K ${GR}/${id}/${id}.result.copynumber.cw_norm.noXY.seg_dup.bed"
#    done < ${GR}/info/${town}.txt;
#
#    multiIntersectBed -i $K > ${GR}/stats/${town}.seg_dup.ovl.bed 
#done

#Count common segdups

#cat ${GR}/stats/novgorod.seg_dup.ovl.bed | awk '{if ($4==20) print $0}' > ${GR}/stats/novgorod.seg_dup.ovl.COMMON.bed
#cat ${GR}/stats/pskov.seg_dup.ovl.bed | awk '{if ($4==22) print $0}' > ${GR}/stats/pskov.seg_dup.ovl.COMMON.bed
#cat ${GR}/stats/yakutsk.seg_dup.ovl.bed | awk '{if ($4==12) print $0}' > ${GR}/stats/yakutsk.seg_dup.ovl.COMMON.bed

seqdup_ovl=${GR}"/stats/all.seg_dup.ovl.bed"
#multiIntersectBed -i ${GR}/stats/novgorod.seg_dup.ovl.COMMON.bed ${GR}/stats/pskov.seg_dup.ovl.COMMON.bed ${GR}/stats/yakutsk.seg_dup.ovl.COMMON.bed > ${seqdup_ovl}

#novgorod=$(awk '{if ($5==1) print $0}' ${seqdup_ovl}| wc -l)
#pskov=$(awk '{if ($5==2) print $0}' ${seqdup_ovl} | wc -l)
#yakutsk=$(awk '{if ($5==3) print $0}' ${seqdup_ovl} | wc -l)

#np=$(awk '{if ($5=="1,2") print $0}' ${seqdup_ovl} | wc -l)
#yp=$(awk '{if ($5=="2,3") print $0}' ${seqdup_ovl} | wc -l)
#ny=$(awk '{if ($5=="1,3") print $0}' ${seqdup_ovl} | wc -l)

#npy=$(awk '{if ($5=="1,2,3") print $0}' ${seqdup_ovl} | wc -l)

#novgorod_bed=$(awk '{if ($5==1) sum+=$3-$2} END {print sum}' ${seqdup_ovl})
#pskov_bed=$(awk '{if ($5==2) sum+=$3-$2} END {print sum}' ${seqdup_ovl})
#yakutsk_bed=$(awk '{if ($5==3) sum+=$3-$2} END {print sum}' ${seqdup_ovl})

#np_bed=$(awk '{if ($5=="1,2") sum+=$3-$2} END {print sum}' ${seqdup_ovl})
#yp_bed=$(awk '{if ($5=="2,3") sum+=$3-$2} END {print sum}' ${seqdup_ovl})
#ny_bed=$(awk '{if ($5=="1,3") sum+=$3-$2} END {print sum}' ${seqdup_ovl})

#npy_bed=$(awk '{if ($5=="1,2,3") sum+=$3-$2} END {print sum}' ${seqdup_ovl})


#echo 'novgorod' ${novgorod}, ${novgorod_bed}
#echo 'pskov' ${pskov}, ${pskov_bed}
#echo 'yakutsk' ${yakutsk}, ${yakutsk_bed}

#echo 'novgorod+pskov' ${np}, ${np_bed}
#echo 'yakutsk+pskov' ${yp}, ${yp_bed}
#echo 'novgorod+yakutsk' ${ny}, ${ny_bed}

#echo 'novgorod+pskov+yakutsk' ${npy}, ${npy_bed}

#Overlap segdups with genes
GENES=${GR}"/stats/genes/refseq_genes.exons.oknaming.bed"
GENE_NAMES=${GR}"/stats/genes/Refseq2Gene.hg38.upd.txt"

awk '{if ($5==1) print $0}' ${seqdup_ovl} > tmp 
bedtools intersect -a ${GENES} -b tmp > ${GR}"/stats/genes/novgorod.ovl.bed"
cut -f4 ${GR}"/stats/genes/novgorod.ovl.bed" | sort | uniq > tmp2
grep -f tmp2 ${GENE_NAMES} | cut -f2 | sort | uniq > ${GR}"/stats/genes/novgorod.uniq.names.txt" 
awk '{if ($5==2) print $0}' ${seqdup_ovl} > tmp 
bedtools intersect -a ${GENES} -b tmp > ${GR}"/stats/genes/pskov.ovl.bed"
cut -f4 ${GR}"/stats/genes/pskov.ovl.bed" | sort | uniq > tmp2
grep -f tmp2 ${GENE_NAMES} | cut -f2 | sort | uniq > ${GR}"/stats/genes/pskov.uniq.names.txt"
awk '{if ($5==3) print $0}' ${seqdup_ovl} > tmp 
bedtools intersect -a ${GENES} -b tmp > ${GR}"/stats/genes/yakutsk.ovl.bed"
cut -f4 ${GR}"/stats/genes/yakutsk.ovl.bed" | sort | uniq > tmp2
grep -f tmp2 ${GENE_NAMES} | cut -f2 | sort | uniq > ${GR}"/stats/genes/yakutsk.uniq.names.txt"
awk '{if ($5=="1,2,3") print $0}' ${seqdup_ovl} > tmp
bedtools intersect -a ${GENES} -b tmp > ${GR}"/stats/genes/common.ovl.bed"
cut -f4 ${GR}"/stats/genes/common.ovl.bed" | sort | uniq > tmp2
grep -f tmp2 ${GENE_NAMES} | cut -f2 | sort | uniq > ${GR}"/stats/genes/common.uniq.names.txt"

#rm tmp tmp2
