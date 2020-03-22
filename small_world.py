#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created on 5:44 pm 22.03.20, by Yi Zhang

' small world generator '

__author__ = 'Yi Zhang'

'''
WS-model (Watts & Strogatz model)

Regular structure
high L: high average distance between nodes 
high C: high average clustering coefficient

Random structure
Low L: Low average distance between nodes 
Low C: Low average clustering coefficient

Real world structure
Neither of them above

L_actual = average distance (shortest path length) between pairs of nodes in the given actual network
L_random = average distance (shortest path length) between pairs of nodes in a randomly connected network with the same number of nodes and links.
C_actual = Clustering coefficient of given actual network
C_random = Clustering coefficient of random network

Observation: 

1. L_random is a bit smaller than L_actual
2. C_random is but much smaller than C_actual


Small World:
Low L
High C
'''

'''
Implementation

n (int) – The number of nodes

k (int) – Each node is joined with its k nearest neighbors in a ring topology.

p (float) – The probability of rewiring each edge

Algo:
1. First create a ring over 𝑛 nodes 1.
 
Then each node in the ring is joined to its 𝑘 nearest neighbors 
(or 𝑘−1 neighbors if 𝑘 is odd). 

2. Then shortcuts are created by replacing some edges as follows: 
for each edge (𝑢,𝑣) in the underlying 
“𝑛-ring with 𝑘 nearest neighbors” 
with probability 𝑝 replace it with a new edge (𝑢,𝑤) 
with uniformly random choice of existing node 𝑤.
'''

import networkx as nx
import matplotlib.pyplot as plt
import random
import os

def display_graph(G, i='',nb='', ri='', ne=[], de = [], path='init.png'): #i is the new node added, ne is the list of new edges
    dir = os.getcwd()
    dest_dir = dir + '/small_world/'
    try:
        os.mkdir(dest_dir)
    except OSError:
        # print("Creation of the directory %s failed" % dest_dir)
        pass
    else:
        print("Successfully created the directory %s " % dest_dir)

    pos = nx.circular_layout(G)
    if i == '' and nb =='' and ri == '' and ne == [] and de == []:
        plt.close()
        new_node = []
        rest_nodes = G.nodes()
        new_edges = []
        rest_edges = G.edges()
        nx.draw_networkx_nodes(G, pos, nodelist=rest_nodes, node_color='r')
        nx.draw_networkx_edges(G, pos, edgelist=rest_edges, edge_color='r')
        nx.draw_networkx_labels(G,pos)
        # plt.show()
        plt.savefig('small_world/' + path)
        plt.close()
    else:
        plt.close()
        new_node = [i]
        neighbor_node = [nb]
        random_node = [ri]
        rest_nodes = list (set(G.nodes())-set(new_node)-set(random_node)-set(neighbor_node))
        new_edges = ne
        deleted_edges = de
        rest_edges = list(set(G.edges())-set(new_edges)-set([(b,a) for (a,b) in new_edges])-set(deleted_edges)-set([(b,a) for (a,b) in deleted_edges]))
        nx.draw_networkx_nodes(G, pos, nodelist=new_node, node_color='g')
        nx.draw_networkx_nodes(G, pos, nodelist=neighbor_node, node_color='y')
        nx.draw_networkx_nodes(G, pos, nodelist=random_node, node_color='c')
        nx.draw_networkx_nodes(G,pos,nodelist=rest_nodes, node_color='r')
        nx.draw_networkx_edges(G, pos, edgelist=deleted_edges, edge_color='y', style='dashdot')
        nx.draw_networkx_edges(G,pos,edgelist=new_edges,edge_color='g',style='dashdot')
        nx.draw_networkx_edges(G,pos,edgelist=rest_edges,edge_color='r')
        nx.draw_networkx_labels(G, pos)
        # plt.show()

        plt.savefig('small_world/'+path)
        plt.close()

# neighbors in round

def round_k_neighbors(i,k,n): # i is the node [0,n-1]
    left_neighbors = [(i + (-1 * (x+1))) % n for x in range(k//2)][::-1]
    right_neighbors =[(i + (x+1)) % n for x in range(k//2)]
    left_neighbors.extend(right_neighbors)
    return left_neighbors

# generate a ring
def ring_lattice(n,k):
    # init graph
    g = nx.Graph()
    g.add_nodes_from([x for x in range(n)])
    # get neighbors of each node and add edge any neighbor to the node
    for i in g.nodes():
        nb = round_k_neighbors(i,k,n)
        g.add_edges_from([(i,j) for j in nb])
    return g

def small_world(n,k,p=0.001):
    # limit value of k
    if (k<2 or k > n-1 or k == None):
        k = n-1

    g = ring_lattice(n,k)
    display_graph(g,path='init.png')
    t = 0
    for v in range(n):
        for nb in g[v]:
            if nb > v:
                random_node = random.randint(0,n-1)
                if (random_node!=v) and (random_node not in [x for x in g[v]]):
                    r = random.random()
                    if r < p:
                        de = [(v,nb)]
                        g.remove_edges_from(de)
                        ne = [(v,random_node)]
                        g.add_edges_from(ne)
                        path = '[' + str(t + 1) + ']' + 'added(' + str(v) + ',' + str(random_node) + ')_removed(' + str(v) + ',' + str(nb) + ')_r=' + str(
                            r) + '.png'
                        display_graph(g, i=v, nb=nb, ri=random_node, ne=ne, de=de,path=path)
                        t += 1
    display_graph(g,path='end.png')

    return g

if __name__ == '__main__':
    g = small_world(20, 6, 0.5)
    print(len(g.edges()))


