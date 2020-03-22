#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created on 2:34 pm 22.03.20, by Yi Zhang

' Random graph generator '

__author__ = 'Yi Zhang'

'''
# Implmentation of random graph generator
# take n, total number of nodes, from the user.
# take p, ie, the value of probability from the user.
# create an empty graph. Add n nodes to it.
# Add edges to the graph randomly.
    # Take a pair of nodes
    # Get a random number r.
    # if r<p , add this edge, else ignore
    # repeat step 1 for all possible pair of nodes.
'''
import networkx as nx
import matplotlib.pyplot as plt
import random
import os

def display_graph(G, i='', ne=[], path='init.png'): #i is the new node added, ne is the list of new edges
    dir = os.getcwd()
    dest_dir = dir + '/random_graph/'
    try:
        os.mkdir(dest_dir)
    except OSError:
        # print("Creation of the directory %s failed" % dest_dir)
        pass
    else:
        print("Successfully created the directory %s " % dest_dir)

    pos = nx.circular_layout(G)
    plt.close()
    if i == '' and ne == []:
        new_node = []
        rest_nodes = G.nodes()
        new_edges = []
        rest_edges = G.edges()
        nx.draw_networkx_nodes(G, pos, nodelist=rest_nodes, node_color='r')
        nx.draw_networkx_edges(G, pos, edgelist=rest_edges, edge_color='r')
        nx.draw_networkx_labels(G,pos)
        # plt.show()
        plt.savefig('random_graph/' + path)
        plt.close()
    else:
        # new_node = [i]
        # rest_nodes = list (set(G.nodes())-set(new_node))
        rest_nodes = G.nodes()
        new_edges = ne
        rest_edges = list(set(G.edges())-set(new_edges)-set([(b,a) for (a,b) in new_edges]))
        #nx.draw_networkx_nodes(G,pos,nodelist=new_node, node_color='g')

        nx.draw_networkx_nodes(G,pos,nodelist=rest_nodes, node_color='r')
        nx.draw_networkx_edges(G,pos,edgelist=new_edges,edge_color='g',style='dashdot')
        nx.draw_networkx_edges(G,pos,edgelist=rest_edges,edge_color='r')
        nx.draw_networkx_labels(G, pos)
        # plt.show()

        plt.savefig('random_graph/'+path)
        plt.close()

def erdos_renyi(G,p=0.001):
    t = 0
    for i in G.nodes():
        for j in G.nodes():
            if i != j:
                r = random.random()
                if r<=p:
                    G.add_edge(i,j)
                    ne = [(i,j)]
                    path = '['+str(t+1)+']'+'ne_added_' + '('+str(i)+','+str(j)+')'+'r='+str(r)+'.png'
                    display_graph(G,ne=ne,path=path)
                    t +=1
                else:
                    # path = '['+str(t+1)+']'+'ne_not_added_' + '('+str(i)+','+str(j)+')'+'p='+str(r)+'.png'
                    # display_graph(G,path=path)
                    t += 1
                    continue

def random_graph_generator(n,p):

    G = nx.Graph()
    G.add_nodes_from([x for x in range(n)])
    display_graph(G,i='',ne=[])
    erdos_renyi(G,p)
    display_graph(G,i='',ne=[],path='end.png')
if __name__ == "__main__":
    # test
    g = random_graph_generator(20, 0.05)