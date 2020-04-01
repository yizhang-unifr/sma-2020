# Real World Network Simulation

## Project of social media analytics 2020

### Aim:

The aim of this project is to implement a tool for simulating real world networks. The tool should be able to:

- Load a social graph
- Run a number of models for approximating real networks
- Visualize the simulated networks

### Tasks:

#### 0. Requirments

```python
# required libs
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import binom
import numpy as np
import pickle

# model generator and helper functions
from random_graph import random_graph_generator
from small_world import small_world
from helper import timer,description
```

#### 1. Dataset

##### 1.1 Load the Facebook dataset

> From [http://snap.stanford.edu/data/egonets-Facebook.html](http://snap.stanford.edu/data/egonets-Facebook.html)

Download facebook_combined.txt dataset in the same directory

```python

```


#### 2.  Instructions on how to run the project

##### 2.1 Required libraries
```
pip install -r requirements.txt
```
##### 2.2 run the project
```
python facebook.py
```

#### 3. Results explanation


##### 3.1 generated file results

```
After the execution stops, you get the following results.

The file 'facebook_dd.png' is the degree distribution of facebook network.
The file 'facebook_network.png' is the visualisation of the facebook network.

The file 'r_graph_dd.png' is the degree distribution of the random graph model.
The file 'random_graph_network.png' is the visualisation of the random graph model.

The file 's_world_dd.png' is the degree distribution of the small world model.
The file 'small_world_network.png' is the visualisation of the small world model.
```

##### 3.2 generated console results example

```
Nodes: 4039
Edges:  88234
Power law regression : y = x^(0.119603)*(-42.776243)+91.555318
Finished Calculation of average path length (Facebook Network) in 0 days, 4 minutes and 2.380 seconds
Average path length of facebook network is: 3.6925
Finished Calculation of average clustering coefficient (Facebook Network) in 0 days, 0 minutes and 2.574 seconds
Average clustering coefficient of facebook network is: 0.6055
Average degree of facebook network is 43.6910
Correspondent p = 0.0108
Random Graph : 
Edges = 175239
Small World : 
Edges = 84819
```
