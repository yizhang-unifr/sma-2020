#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created on 12:07 am 30.03.20, by Yi Zhang

' Explore the properties of the graph from facebook. '

__author__ = 'Yi Zhang'

import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import binom
import numpy as np
from random_graph import random_graph_generator
from small_world import small_world
import pickle
from helper import timer,description

# load edge list

path = 'facebook_combined.txt'
facebook_g = nx.read_edgelist(path=path)



# Degree Distribution

def func_powerlaw(x, m, c, c0):
    return c0 + x**m * c


# plot degree distribution
def plot_dd(dd, reg_plot = True, regression=None, path='facebook',label = None, color = 'r'):
    y = dd
    x = list(range(len(y)))
    if reg_plot == True:
        if regression is None: # if None, power law
            p_opt, p_cov = curve_fit(func_powerlaw, x, y)
            print('Power law regression : y = x^(%f)*(%f)+%f' % tuple(p_opt))
            regression = [func_powerlaw(i, *p_opt) for i in x if func_powerlaw(i, *p_opt) > 0]
        else:
            regression = regression
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Degrees')
    ax.set_ylabel('Number of counts')
    ax.bar(x,y,label='Counts on degree')
    if reg_plot == True:
        if label is None:
            ax.plot(x[:len(regression)],regression,color=color,label='Power law regression')
        else:
            ax.plot(x[:len(regression)], regression, color=color, label=label, linestyle='dashed')
    ax.legend()
    plt.savefig(path+'_dd.png')
    # plt.show()


def plot_graph(g,title, color='blue',path='facebook_network'):
    plt.figure(figsize=(8, 6))
    pos_random = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos=pos_random, node_size=1, node_color=color)
    nx.draw_networkx_edges(g, pos=pos_random, alpha=0.01)
    plt.axis('off')
    plt.title(title)
    plt.savefig(path+'.svg',dpi=1000)
    plt.savefig(path+'.png',dpi=1000)

    # plt.show()

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

# function for task 2

def C(d): # Clustering coefficient of ring lattice
    return 3*(d-2)/(4*(d-1))

def beta_func(cc,d):
    beta = 1 - pow(cc/C(d),(1/3))
    return beta

# random graph

# Average Path Length (!Time-consuming!)

@timer
@description('Calculation of average path length (Random Graph)')
def get_r_graph_apl(g):
    res = nx.average_shortest_path_length(g)
    return res

# Clustering Coefficient
@timer
@description('Calculation of average clustering coefficient (Random Graph)')
def get_r_graph_cc(g):
    res = nx.average_clustering(g)
    return res

# Small World

# Average Path Length (!Time-consuming!)

@timer
@description('Calculation of average path length (Small World)')
def get_s_world_apl(g):
    res = nx.average_shortest_path_length(g)
    return res

# Clustering Coefficient
@timer
@description('Calculation of average clustering coefficient (Small World)')
def get_s_world_cc(g):
    res = nx.average_clustering(g)
    return res

def dd_analyzer(dd_list):
    dd_len = len(dd_list)
    dd_sum = sum(dd_list)
    dd_max = max(dd_list)
    dd_max_ind = dd_list.index(dd_max)
    dict = {
        'max degree' : dd_len,
        'total nodes' : dd_sum,
        'most often degree' : dd_max_ind,
        'most often degree counts' : dd_max,
    }
    return dict

if __name__ == '__main__':
    # Number of Nodes
    number_of_nodes = len(facebook_g.nodes)
    print("#Nodes:", number_of_nodes)
    # Number of Edges
    number_of_edges = len(facebook_g.edges)
    print('#Edges: ', number_of_edges)
    # Plot
    degree_distribution_list = nx.degree_histogram(facebook_g)

    plot_dd(degree_distribution_list)
    # Get Average Path Length (!Time-consuming!)
    facebook_apl = get_facebook_apl(facebook_g)
    print('Average path length of facebook network is: %.4f' % facebook_apl)

    # Get Average Clustering Coefficient (!Time-consuming!)
    facebook_cc = get_facebook_cc(facebook_g)
    print('Average clustering coefficient of facebook network is: %.4f' % facebook_cc)

    # plot facebook network
    plot_graph(facebook_g,title='Facebook network',color='red')
    facebook_dd_dict = dd_analyzer(degree_distribution_list)
    print('facebook degree distribution:', facebook_dd_dict)

    avg_degree = number_of_edges*2/number_of_nodes
    print("Average degree of facebook network is %0.4f" %  avg_degree)

    '''
    Output: Facebook
    #Nodes: 4039
    #Edges:  88234
    Power law regression : y = x^(0.119603)*(-42.776247)+91.555322
    Finished Calculation of Average path length (Facebook Network) in 0 days, 5 minutes and 2.912 seconds
    Average path length of facebook network is: 3.6925
    Finished Calculation of average clustering coefficient (Facebook Network) in 0 days, 0 minutes and 2.659 seconds
    Average clustering coefficient of facebook network is: 0.6055
    facebook degree distribution: {'max degree': 1046, 'total nodes': 4039, 'most often degree': 8, 'most often degree counts': 111}
    Average degree of facebook network is 43.6910
    '''

    def init_random_graph():
        p = avg_degree / (number_of_nodes - 1)
        print("Correspondent p = %0.4f" % p)
        r_graph = random_graph_generator(number_of_nodes,p)
        r_graph_dd_list = nx.degree_histogram(r_graph)
        max_ind = r_graph_dd_list.index(max(r_graph_dd_list))
        r_x = list(range(len(r_graph_dd_list)))
        r_regression = binom.pmf(r_x,number_of_nodes,p=p)*(number_of_nodes-1)
        reg_max_ind = np.argmax(r_regression)
        shift = max_ind-reg_max_ind
        # handle the shift
        if shift>0: # shift right
            r_regression = np.concatenate((np.zeros((shift,)), r_regression[:len(r_regression)-shift]))
        else: # shift left
            r_regression = np.concatenate((r_regression[(-shift):], np.zeros((-shift,))))
        plot_dd(r_graph_dd_list,regression=r_regression, path='r_graph',color='tab:orange',label='Approx. Binomial Distribution')

        r_graph_apl = get_r_graph_apl(r_graph)
        print('Average path length of random graph network is: %.4f' % r_graph_apl)

        r_graph_cc = get_r_graph_cc(r_graph)
        print('Average clustering coefficient of random graph network is: %.4f' % r_graph_cc)

        # save random_graph
        r_graph_dict = {
            'p': p,
            'r_graph': r_graph,
            'r_graph_apl':r_graph_apl,
            'r_graph_cc':r_graph_cc
        }

        with open('random_graph.data', 'wb') as rg:
            pickle.dump(r_graph_dict, rg)
        return r_graph_dict

    try:
        with open('random_graph.data', 'rb') as rg:
            r_graph_dict = pickle.load(rg)
    except IOError:
        print("No files found. Re-building... ")
        r_graph_dict= init_random_graph()
    finally:
        p = r_graph_dict['p']
        r_graph = r_graph_dict['r_graph']
        r_graph_apl = r_graph_dict['r_graph_apl']
        r_graph_cc = r_graph_dict['r_graph_cc']
        print('Random Graph : \n#Edges = %s' % len(r_graph.edges))

    plot_graph(r_graph,title='Random graph',color='blue',path='random_graph_network')
    r_graph_dd_dict = dd_analyzer(nx.degree_histogram(r_graph))
    print('random graph degree distribution:', r_graph_dd_dict)

    '''
    Output: Random Graph
    Average degree of facebook network is 43.6910
    Correspondent p = 0.0108
    Finished Calculation of average path length (Random Graph) in 0 days, 5 minutes and 33.065 seconds
    Average path length of random graph network is: 2.6078
    Finished Calculation of average clustering coefficient (Random Graph) in 0 days, 0 minutes and 1.293 seconds
    Average clustering coefficient of random graph network is: 0.0108
    Random Graph : 
    #Edges = 87935
    random graph degree distribution: {'max degree': 70, 'total nodes': 4039, 'most often degree': 42, 'most often degree counts': 271}
    '''

    # Small world
    def init_small_world():
        beta = beta_func(facebook_cc, avg_degree)
        print('Correspondent beta = %.4f' % beta)
        s_world = small_world(number_of_nodes,int(avg_degree),beta)
        s_world_dd_list =nx.degree_histogram(s_world)
        plot_dd(s_world_dd_list,reg_plot=False, path='s_world', color='m',
                label='Approx. Binomial Distribution' )

        s_world_apl = get_s_world_apl(s_world)
        print('Average path length of small world network is: %.4f' % s_world_apl)

        s_world_cc = get_s_world_cc(s_world)
        print('Average clustering coefficient of small world network is: %.4f' % s_world_cc)

        # save small_world
        s_world_dict = {
            'beta': beta,
            's_world': s_world,
            's_world_apl': s_world_apl,
            's_world_cc': s_world_cc
        }

        with open('small_world.data', 'wb') as sw:
            pickle.dump(s_world_dict, sw)

        return s_world_dict

    try:
        with open('small_world.data', 'rb') as sw:
            s_world_dict = pickle.load(sw)
    except IOError:
        print("No files found. Re-building... ")
        s_world_dict = init_small_world()
    finally:
        beta = s_world_dict['beta']
        s_world = s_world_dict['s_world']
        s_world_apl = s_world_dict['s_world_apl']
        s_world_cc = s_world_dict['s_world_cc']
        print('Small World : \n#Edges = %s' % len(s_world.edges))

    s_world_dd_dict = dd_analyzer(nx.degree_histogram(s_world))
    print('small world degree distribution:', s_world_dd_dict)
    plot_graph(s_world,title='Small world',color='green',path='small_world_network')

    '''
    Output: small world
    Correspondent beta = 0.5575
    Finished Calculation of average path length (Small World) in 0 days, 5 minutes and 47.604 seconds
    Average path length of small world network is: 2.6817
    Finished Calculation of average clustering coefficient (Small World) in 0 days, 0 minutes and 1.039 seconds
    Average clustering coefficient of small world network is: 0.6126
    Small World : 
    #Edges = 84819
    small world degree distribution: {'max degree': 49, 'total nodes': 4039, 'most often degree': 42, 'most often degree counts': 1144}
    '''


