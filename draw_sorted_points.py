#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import sys
import collections

path = sys.argv[1]
def parse_points(path):
    res = []
    with open(path) as f:
        for line in f:
            line = line.strip().split()
            res.append((int(line[1]), int(line[0])))
    return res

res  = parse_points(path)
res = sorted(res, key=lambda a: a[0])
x = map(lambda a: a[0], res)
y = map(lambda a: a[1], res)
plt.plot(x, y, 'go-')
plt.xlabel('# reads')
plt.ylabel('Score')
plt.savefig('points')
