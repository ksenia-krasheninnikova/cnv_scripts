#!/usr/bin/env bash


for e in $(ls /mnt/genomerussia/ssidorov/bakeoff/illumina/bam/illumina.JH-027F.deduped.sorted.bam); do
    filename=$(basename "$e");
    echo $filename
    readgroup="${filename%.*.*.*}";
    echo $readgroup
    samtools addreplacerg -r 'ID:'${readgroup} -r 'LB:'${readgroup} -r 'SM:'${readgroup} -o '/mnt/genomerussia/ksenia/bakeoff/raw_reads/'${readgroup}'.bam' $e;
done
