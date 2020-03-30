#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created on 12:07 am 30.03.20, by Yi Zhang

' Explore the properties of the graph from facebook. '

__author__ = 'Yi Zhang'

import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from random_graph import random_graph_generator
from small_world import small_world
import pickle
from helper import timer,description

# load edges

path = 'facebook_combined.txt'
facebook_g = nx.read_edgelist(path=path)



# Degree Distribution

def func_powerlaw(x, m, c, c0):
    return c0 + x**m * c


# plot degree distribution
def plot_dd(dd):
    y = dd
    x = list(range(len(y)))
    p_opt,p_cov = curve_fit(func_powerlaw, x, y)
    print('Power law regression : y = x^(%f)*(%f)+%f' % tuple(p_opt))
    regression = [func_powerlaw(i,*p_opt) for i in x if func_powerlaw(i,*p_opt)>0]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(x,y)
    ax.plot(x[:len(regression)],regression,color='r')
    plt.savefig('facebook_dd.png')
    plt.show()

# Average Path Length (!Time-consuming!)

@timer
@description('Calculation of average path length (Facebook Network)')
def get_facebook_apl(g):
    res = nx.average_shortest_path_length(g)
    return res

# Clustering Coefficient
@timer
@description('Calculation of average clustering coefficient (Facebook Network)')
def get_facebook_cc(g):
    res = nx.average_clustering(g)
    return res

if __name__ == '__main__':
    # Number of Nodes
    number_of_nodes = len(facebook_g.nodes)
    print("#Nodes:", number_of_nodes)
    # Number of Edges
    number_of_edges = len(facebook_g.edges)
    print('#Edges: ', number_of_edges)
    # Plot
    degree_distribution_list = nx.degree_histogram(facebook_g)

    '''
    Output
    #Nodes: 4039
    #Edges:  88234
    Power law regression : y = x^(0.119603)*(-42.776247)+91.555322
    '''

    plot_dd(degree_distribution_list)
    # Get Average Path Length (!Time-consuming!)
    facebook_apl = get_facebook_apl(facebook_g)
    print('Average path length of facebook network is: %.4f' % facebook_apl)
    '''
    Output:
    Finished Calculation of Average path length (Facebook Network) in 0 days, 5 minutes and 2.912 seconds
    Average path length of facebook network is: 3.6925
    '''
    # Get Average Clustering Coefficient (!Time-consuming!)
    facebook_cc = get_facebook_cc(facebook_g)
    print('Average clustering coefficient of facebook network is: %.4f' % facebook_cc)

    '''
    Output
    Finished Calculation of average clustering coefficient (Facebook Network) in 0 days, 0 minutes and 2.659 seconds
    Average clustering coefficient of facebook network is: 0.6055
    '''
