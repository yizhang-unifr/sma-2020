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
import os
import random

import matplotlib.pyplot as plt
import networkx as nx


def display_graph(graph, i='', added_new_node=None, path='init.png'):  # added_new_node is the new node added, list_of_new_edges is the list of new edges
    if added_new_node is None:
        added_new_node = []
    _dir = os.getcwd()
    dest_dir = _dir + '/random_graph/'
    try:
        os.mkdir(dest_dir)
    except OSError:
        # print("Creation of the directory %s failed" % dest_dir)
        pass
    else:
        print("Successfully created the directory %s " % dest_dir)

    pos = nx.circular_layout(graph)
    plt.close()
    if i == '' and added_new_node == []:
        new_node = []
        rest_nodes = graph.nodes()
        new_edges = []
        rest_edges = graph.edges()
        nx.draw_networkx_nodes(graph, pos, nodelist=rest_nodes, node_color='r')
        nx.draw_networkx_edges(graph, pos, edgelist=rest_edges, edge_color='r')
        nx.draw_networkx_labels(graph, pos)
        # plt.show()
        plt.savefig('random_graph/' + path)
        plt.close()
    else:
        # new_node = [added_new_node]
        # rest_nodes = list (set(graph.nodes())-set(new_node))
        rest_nodes = graph.nodes()
        new_edges = added_new_node
        rest_edges = list(set(graph.edges()) - set(new_edges) - set([(b, a) for (a, b) in new_edges]))
        # nx.draw_networkx_nodes(graph,pos,nodelist=new_node, node_color='g')

        nx.draw_networkx_nodes(graph, pos, nodelist=rest_nodes, node_color='r')
        nx.draw_networkx_edges(graph, pos, edgelist=new_edges, edge_color='g', style='dashdot')
        nx.draw_networkx_edges(graph, pos, edgelist=rest_edges, edge_color='r')
        nx.draw_networkx_labels(graph, pos)
        # plt.show()

        plt.savefig('random_graph/' + path)
        plt.close()


def erdos_renyi(graph, p=0.001, display_steps=False):
    t = 0
    for i in graph.nodes():
        for j in graph.nodes():
            if i != j:
                r = random.random()
                if r <= p:
                    graph.add_edge(i, j)
                    ne = [(i, j)]
                    if display_steps==True:
                        path = '[' + str(t + 1) + ']' + 'ne_added_' + '(' + str(i) + ',' + str(j) + ')' + 'r=' + str(
                        r) + '.png'

                        display_graph(graph, added_new_node=ne, path=path)
                    t += 1
                else:
                    # path = '['+str(t+1)+']'+'ne_not_added_' + '('+str(added_new_node)+','+str(j)+')'+'p='+str(r)+'.png'
                    # display_graph(graph,path=path)
                    t += 1
                    continue
    return graph


def random_graph_generator(n, p, display_steps=False):
    graph = nx.Graph()
    graph.add_nodes_from([x for x in range(n)])
    display_graph(graph, i='', added_new_node=[])
    res = erdos_renyi(graph, p, display_steps)
    display_graph(graph, i='', added_new_node=[], path='end.png')
    return res


if __name__ == "__main__":
    # test
    random_graph_generator(20, 0.05)
