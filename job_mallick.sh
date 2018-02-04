#!/bin/bash

prefix_from_reads='/mnt/sochi/gtamazian/mallick/'
reference='/home/genomerussia/tools/cnv_scripts/reference/hg38.kmers_36_5_overrepresented_kmers_padding_36bp.chrs.fa'
work_dir_pref='/mnt/sochi/ksenia/mallick/'
destination='/mnt/sochi/ksenia/mallick/cnv/sv/'
conf='/home/genomerussia/tools/cnv_scripts/reference/hg38.conf'
path_script='/home/genomerussia/tools/cnv_scripts/bin/run_individuals_fastq_mapping'

id=$1
echo "job id:" $job_id "sample id" ${id}
work_dir=${work_dir_pref}/${id}
mkdir ${work_dir}
cp ${prefix_from_reads}/${id}_1.fastq.gz ${work_dir}
cp ${prefix_from_reads}/${id}_2.fastq.gz ${work_dir}
gunzip ${work_dir}/*.gz
${path_script} ${work_dir}/${id}_1.fastq ${work_dir}/${id}_2.fastq ${reference} $id ${work_dir}  ${destination}${id} ${conf} --threads 10
#rm -r ${work_dir}
