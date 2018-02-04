#!/usr/bin/env python

import sys
from collections import Counter

path = sys.argv[1]
 
res = []
with open(path) as f:
    for line in f:
        line = line.strip().split(':')
        for e in line:
            e = e.split('|')
            res.append(e[0])
res = Counter(res)
for x in res.keys():
    print x, ':', res[x]
