#!/usr/bin/env python

import argparse
import math
import numpy

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
        
def search_for_sd(data, mean, sd):
    bound = mean + 3 * sd
    low_bound = mean + 2 * sd
    i = 0 
    all_length = 0
    while i < len(data):
        start = i
        low_bound_cnt = 0
        cn = float(data[i][4])
        while cn > low_bound and i < len(data):
            if cn > 100:
               i+=1
               if i < len(data) - 1:
                cn = float(data[i][4])
               continue
            if data[start][0] != data[i][0]:
                #i = i - 1
                break
            if cn < bound:
                if low_bound_cnt == 1:
                    break
                low_bound_cnt += 1
            i += 1
            if i < len(data) - 1:
                cn = float(data[i][4])
        if i - 1 - start > 4:
           length = int(data[i-1][2])-int(data[start][1])
           if length >= 10000:
               print data[start][0]+'\t'+data[start][1]+'\t'+data[i-1][2]
               all_length += length
        i += 1
    print all_length
            
def cut_window(tail, window_size=1000):
    size = 0
    portion = window_size
    window = []
    i = 0
    while i < len(tail) and portion > 0:
        if int(tail[i][2]) - int(tail[i][1]) > portion:
            paste = list(tail[i])
            paste[2] = int(tail[i][1])+portion
            window.append(paste)
            tail[i][1] = int(tail[i][1])+portion+1 
            i -= 1
            break
        if int(tail[i][2]) - int(tail[i][1]) == portion:
            window.append(tail[i])
            break
        if int(tail[i][2]) - int(tail[i][1]) < portion:
            portion -= int(tail[i][2]) - int(tail[i][1])
            window.append(tail[i])
            i += 1
    return tail[i+1:], window
    

def split_into_windows(scaffold_regions, window_size=1000):
    tail = scaffold_regions
    l = []
    while tail:
        tail, window = cut_window(tail, window_size)
        l.append(window)
    return l

def search_for_sd_window_based(data, mean, sd):
    bound = mean + 3 * sd
    low_bound = mean + 2 * sd   
    i = 0
    scaffolds = set([e[0] for e in data])
    for s in scaffolds:
        window_size = 0
        scaffold_regions = filter(lambda x: x[0] == s, data)
        copy_numbers = []
        windows_copy_number_values = []
        windows = split_into_windows(scaffold_regions, window_size=1000)
        window_counter = 0
        low_window_counter = 0
        seg_dup = []
        for w in windows:
            #print w
            cn = numpy.mean([float(x[4]) for x in w])
            if cn > low_bound and cn < bound:
                if low_window_counter == 1:
                    #size = sum([int(x[2]) - int(x[1]) for e in seg_dup for x in e ])
                    #if window_counter > 4 and size > 10000:
                    if window_counter > 4 and int(seg_dup[-1][-1][2]) - int(seg_dup[0][0][1]) > 10000:
                        #print seg_dup
                        print s+'\t'+ str(seg_dup[0][0][1])+'\t'+ str(seg_dup[-1][-1][2])
                    low_window_counter = 0
                    window_counter = 0
                    seg_dup =  []
                    continue
                low_window_counter += 1
                seg_dup.append(w)
            elif cn < low_bound:
                if seg_dup and window_counter > 4 and low_window_counter < 2:
                    #size = sum([int(x[2]) - int(x[1]) for e in seg_dup for x in e ])
                    #if size > 10000:
                    if int(seg_dup[-1][-1][2]) - int(seg_dup[0][0][1]) > 10000:
                        #print seg_dup
                        print s+'\t'+ str(seg_dup[0][0][1])+'\t'+ str(seg_dup[-1][-1][2])
                low_window_counter = 0
                window_counter = 0
                seg_dup = []
                continue
            elif cn > 100:
                continue
            elif cn > bound:
                window_counter += 1
                seg_dup.append(w)
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    data = parse_input(args.path)
    cn, total = get_cn_in_controls(data)
    mean = get_mean(cn, total)
    sd = get_standart_dev(cn, total, mean)
#    print 'mean =', mean, 'sd = ', sd
    search_for_sd_window_based(data, mean, sd)
