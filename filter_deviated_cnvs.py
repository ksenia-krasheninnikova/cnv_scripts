#!/usr/bin/env python

import argparse
import math
import numpy
from find_segdups import parse_input,get_cn_in_controls, get_standart_dev, get_mean

def get_cn_in_controls(data):
    cn = []
    lengths = []
    for e in data:
        if e[-1] == 'Y':
            length = int(e[2])-int(e[1])
            cn.append(float(e[4]))
            lengths.append(length)
    return cn, lengths
     
def get_mean(cn_controls, total_length):
    s = sum(map(lambda x: x[0]*x[1], zip(cn_controls, total_length)))
    return s/sum(total_length)

def get_standart_dev(cn_controls, total_length, mean):
    s = 0.0
    for e,l in zip(cn_controls, total_length):
        s += l * (e - mean) * (e - mean)
    return math.sqrt(s/sum(total_length))

def parse_input(input):
    data = []
    with open(input) as f:
        f.readline()
        f.readline()
        for line in f:
            data.append(line.strip().split())
    return data
        

def filter_deviated(data, mean, sd):
    upper_bound = mean + 3 * sd   
    #or?lower_bound = mean - 3 * sd    
    lower_bound = float(mean)/2  
    for cnv in data:
        if float(cnv[4]) > upper_bound:
            print '\t'.join(cnv+['upper'])
        if float(cnv[4]) < lower_bound:
            print '\t'.join(cnv+['lower'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    data = parse_input(args.path)
    cn, total = get_cn_in_controls(data)
    mean = get_mean(cn, total)
    #print 'mean', mean
    sd = get_standart_dev(cn, total, mean)
    #print 'sd', sd
    filter_deviated(data, mean, sd)
