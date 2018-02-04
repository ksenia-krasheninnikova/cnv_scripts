#!/usr/bin/env python

'''
count Vst as (Vt - Vs)/Vt
Vt is the variance among all unrelated individuals in two populations
Vs is the average variance within each population weighted for population size
'''

from argparse import ArgumentParser
import numpy

def parse_cnvs(path, chrom):
    cnvs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or '#' == line[0]:
                continue
            line = line.split()
            if line[0] == chrom:
                cnvs.append((int(line[1]),int(line[2]),float(line[4])))
    return cnvs

def handle_population(path, chrom):
    paths = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or '#' == line[0]:
                continue
            paths.append(line)
    collection = []
    for path in paths:
        collection.append(parse_cnvs(path, chrom))
    return collection

#def get_log2ratio(a,b):
#    return numpy.log2(a) / numpy.log2(b)

def get_chromosome_size(size_file, chrom):
        with open(size_file) as f:
            for line in f:
                line = line.strip().split()
                if line[0] == chrom:
                    return int(line[1])
        return -1 

def get_cnv_at_pos(individ, pos, window):
    counter = 0
    acc = 0
    start = pos
    end = pos+window
    for entry in individ:
        if entry[0] <= start and start <= entry[1] and entry[1] <= end:
            acc += entry[-1] * (entry[1] - start)
            counter += entry[1] - start
        elif start <= entry[0] and entry[0] <= end and end <= entry[1]:
            acc += entry[-1] * (end - entry[0])
            counter += end - entry[0]
    if counter == 0: return -1
    return acc/counter

def get_Vs(collection, k, window) :
    cnvs = []
    for i in range(len(collection)):
        individ = collection[i]
        cnv = get_cnv_at_pos(individ, k, window)
        if cnv == -1:
            continue
        cnvs.append(cnv)
    return numpy.var(cnvs)


def get_Vt(collection1, collection2, k, window):
    cnvs = []
    for individ in collection1 + collection2:
        cnv = get_cnv_at_pos(individ, k, window)
        if cnv == -1:
            continue
        cnvs.append(cnv)
    return numpy.var(cnvs)
 
if __name__ == '__main__' :
    parser = ArgumentParser()
    parser.add_argument('--sizes', help='file produced with faSize -detailed over human genome')
    parser.add_argument('--chrom', help='choose chromosome to process')
    parser.add_argument('--window', help='nucleotide window')
    parser.add_argument('path1', help='file with paths of the first population')
    parser.add_argument('path2', help='file with paths of the second population')
    parser.add_argument('output')
    args = parser.parse_args()
    size = get_chromosome_size(args.sizes, args.chrom)
    window = int(args.window)
    if size == -1:
        print 'wrong chromosome. exit'
        exit(1)
    collection1 = handle_population(args.path1, args.chrom)
    collection2 = handle_population(args.path2, args.chrom)
    with open(args.output, 'w') as f:
        for pos in range(1, size, window):
            Vs1 = get_Vs(collection1, pos, window)
            Vs2 = get_Vs(collection2, pos, window)
            n1 = len(collection1)
            n2 = len(collection2)
            Vs = (n1*Vs1 + n2*Vs2)/(n1+n2)
            #print 'Vs',Vs,Vs1, Vs2
            Vt = get_Vt(collection1, collection2, pos, window)
            #print 'Vt',Vt
            Vst = 1 - Vs/Vt
            f.write('\t'.join(map(str,[args.chrom, pos, window, Vst]))+'\n') 
