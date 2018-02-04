#!/bin/bash

#parallel -a /mnt/sochi/ksenia/mallick/sample_ids_1.txt './job_mallick.sh {}'
parallel -a /mnt/sochi/ksenia/mallick/sample_ids_2.txt './job_mallick.sh {}'

