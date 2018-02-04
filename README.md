# cnv_scripts
scripts for read-depth cnv annotation

Requires:

1. kentUtils
2. mrfast, mrsfast, mrcanavar http://mrcanavar.sourceforge.net/manual.html
3. samtools
4. bedtools

**Genome Masking**

1. Repeat Finder
2. Tandem Repeat Finder
3. Window Masker
(according to [1])
4. Partition scaffolds and contigs into kmers of 36bp (with adjacent khmers overlapping 5 bps) and map them to the assembly using mrsFast to account for multi mappings’ 
ex.:
```bash
split_assembly_to_substrings  path_to_reference.fa 36 5 > reference.kmers_36_5.fa 

mrsfast --threads 64 --search path_to_reference.fa --seq  reference.kmers_36_5.fa -o reference.kmers_36_5.sam
```

find overrepresented kmers (mapped more than twice)
```bash
 grep -v -e "@SQ" -e "@HD" reference.kmers_36_5.sam  | cut -f10 | uniq -c | sed 's/ \+ //g' | awk '{if ($1 > 2) print;}'> reference.kmers_36_5.lst
```

mask overrepresented kmers
a. filter sam and leave only overrepresented kmers
```bash
for i in `cat reference.kmers_36_5.lst | awk {'print $2'}`; do grep -w ${i} reference.kmers_36_5.sam; done > reference.kmers_36_5_overrepresented_kmers.sam
```
b. get regions from sam to bed
```bash
awk '{if (NF > 10) print $3"\t"$4"\t"$4+36;}'  reference.kmers_36_5_overrepresented_kmers.sam >  reference.kmers_36_5_overrepresented_kmers.bed

samtools view -bT path_to_reference.fa reference.kmers_36_5.sam | samtools sort --threads 5 > reference.kmers_36_5.bam

samtools index reference.kmers_36_5.bam

mkdir kmers_36_5/
#reference lst is the list of scaffolds
while read p; do samtools view -h reference.kmers_36_5.bam $p > kmers_36_5/$p.sam; done < reference.lst

**FIXME: invokes zombie-processes and kills I/O**
find_in_sam_to_bed reference.kmers_36_5.sam reference.kmers_36_5.lst > reference.kmers_36_5.bed

cat kmers_36_5/*.bed > kmers_36_5/all.bed
```

mask from bed
```bash
maskFastaFromBed -fi reference -bed kmers_36_5/all.bed -fo reference.kmers_36_5_overrepresented_kmers.fa
```

5. Importantly, because reads will not map to positions covering regions masked in the reference assembly, read depth will be lower at the edges of these regions, which could underestimate the copy number in the subsequent step. To avoid this, the 36 bps flanking any masked region or gap were masked as well and thus not included within the defined windows.

```bash
mask_padding reference.kmers_36_5_overrepresented_kmers.fa > reference.kmers_36_5_overrepresented_kmers_padding_36bp.fa

mv  reference.kmers_36_5_overrepresented_kmers_padding_36bp.fa  reference.final.fa

samtools faidx reference.final.fa

mrfast --index reference.final.fa
```

6. run prep mode of mrcanavar
get assembly gaps coordinates
ex.: (get script from https://gtamazian.com/2016/06/23/converting-an-agp-file-to-the-bed-format/)

```bash
agp2bed.py hg38.agp hg38.gaps.bed

mrcanavar --prep -fasta reference.final.fa -gaps hg38.gaps.bed -conf reference.conf
```

**Process Individuals**

see run_Mallick.sh script


**References:**

[1] Alkan et al. Personalized Copy-Number and Segmental Duplication Maps using Next-Generation Sequencing, Nature Genetics, 2009
