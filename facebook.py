#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created on 12:07 am 30.03.20, by Yi Zhang

' Explore the properties of the graph from facebook. '

__author__ = 'Yi Zhang'

import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# load edges

path = 'facebook_combined.txt'
facebook_g = nx.read_edgelist(path=path)

# Number of Nodes
number_of_nodes = len(facebook_g.nodes)
print("#Nodes:", number_of_nodes)
# Number of Edges
number_of_edges = len(facebook_g.edges)
print('#Edges: ', number_of_edges)

# Degree Distribution

def func_powerlaw(x, m, c, c0):
    return c0 + x**m * c

degree_distribution_list = nx.degree_histogram(facebook_g)
y= degree_distribution_list

print(degree_distribution_list)

# plot degree distribution
x = list(range(len(y)))
p_opt,p_cov = curve_fit(func_powerlaw, x, y)
print('Power law regression : y = x^(%f)*(%f)+%f' % tuple(p_opt))
regression = [func_powerlaw(i,*p_opt) for i in x if func_powerlaw(i,*p_opt)>0]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(x,y)
ax.plot(x[:len(regression)],regression,color='r')
plt.show()

# Average Path Length

# Clustering Coefficient


