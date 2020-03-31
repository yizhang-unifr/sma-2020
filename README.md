# Real World Network Simulation

## Project of social media analytics 2020

### Aim:

The aim of this project is to implement a tool for simulating real world networks. The tool should be able to:

- Load a social graph
- Run a number of models for approximating real networks
- Visualize the simulated networks

### Tasks:

#### 0. Dependencies and structures

- Dependencies

    In this project, `networkx` and `matplotlib` will be required as core dependencies. All dependencies are listed in the following

```python
# required libs
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import binom
import numpy as np
import pickle
```

- User defined modules are the 2 model generators and a helper modules to 

```python
# model generator and helper functions
from random_graph import random_graph_generator
from small_world import small_world
from helper import timer,description
```

- Main entry point is `facebook.py`

#### 1. Dataset

##### 1.1 Load the Facebook dataset

From [http://snap.stanford.edu/data/egonets-Facebook.html](http://snap.stanford.edu/data/egonets-Facebook.html) we have downloaded and unzip the file `'facebook_combined.txt.gz'` to `'facebook_combined.txt'`. Then, we copy it to the root folder of project. With the following script we load the edge list and generate the graph of the given real world facebook network

```python
path = 'facebook_combined.txt'
facebook_g = nx.read_edgelist(path=path)
```

##### 1.2 Explore the properties of the graph.

In this section, we explored the following properties of the graphs:

- Number of nodes = 4039

```python
# Number of Nodes
number_of_nodes = len(facebook_g.nodes)
print("#Nodes:", number_of_nodes)

'''
Output
#Nodes: 4039
'''
```

- Number of edges = 88234

```python
# Number of Edges
number_of_edges = len(facebook_g.edges)
print('#Edges: ', number_of_edges)

'''
Output
#Edges:  88234
'''
```

- Average degree of graphs = 43.6910

According to the definition of average degree of graphs(1) and definition of degree of graphs (2):
$$
\begin{aligned}    
    \bar{d_g} & = \frac{1}{n}\sum_{i=1}^{n}{d_i} & & &(1)\\
    \sum_{i=1}^{n}{d_i} & = 2 \times |E| & & & (2)\\
\end{aligned}
$$
Combining (1) and (2)
We have:
$$
    \bar{d_g} = \frac{2}{n} |E| 
$$
where $n$ is number of nodes, $d_i$ is the degree of vertice $v_i$ and $|E|$ is the number of edges.

```python
avg_degree = number_of_edges*2/number_of_nodes
print("Average degree of facebook network is %0.4f" %  avg_degree)

'''
Output
Average degree of facebook network is 43.6910
'''
```

- Average path length of graphs = 3.6925

According to the definition of average path length we obtain

$$
\textnormal{Average path length}: \bar{l}_G = \frac{1}{n(n-1)} \cdot \sum_{i\neq j}d(v_i,v_j)
$$

where $n$ is the number of vertices, $d(v_i, v_j)$ is the shortest path length from $v_i$ to $v_j$

```python
@timer
@description('Calculation of average path length (Facebook Network)')
def get_facebook_apl(g):
    res = nx.average_shortest_path_length(g)
    return res
facebook_apl = get_facebook_apl(facebook_g)
    print('Average path length of facebook network is: %.4f' % facebook_apl)
'''
Output
Finished Calculation of Average path length (Facebook Network) in 0 days, 5 minutes and 2.912 seconds
Average path length of facebook network is: 3.6925
'''
```



- Cluster coefficient = 0.6055



$$
\bar{C}(g) = \frac{1}{n}\sum_{i=1}^{n}{\frac{\textnormal{\#connected pairs of } v \textnormal{'s neighbors}}{\textnormal{\#pairs of }v \textnormal{'s neighbors}}}
$$


