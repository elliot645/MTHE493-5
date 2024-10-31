from utils.graphutils import Graph, Node, create_county_adjacency_dict
import networkx as nx
import random
from utils.polya_process import polya
import time
import matplotlib.pyplot as plt

state_name = 'NV'

st = time.time()*1000

neighbours = create_county_adjacency_dict("data\countyadj.csv")
t1 = time.time()*1000
print(f"Reading Data: {int(t1-st)}ms")

county_graph = Graph()

#set up graph
for state in neighbours:
    for county in neighbours[state]:
        population = random.uniform(500,10000)
        red = int(random.uniform(0,population))
        blue = population - red
        county_graph.add_node(Node(id=county,state=state,red=red,blue=blue,population=population,neighbours = neighbours[state][county]))

t2 = time.time()*1000
print(f"Building Graph: {int(t2-t1)}ms")

county_graph.visualize_graph(state_name)
county_graph.graph_node_opinions(state_name)

t3 = time.time()*1000
#Feed into polya model
county_graph, results = polya(county_graph,100,50000,state_name)
t4 = time.time()*1000
print(f"Running Polya Process: {int(t4-t3)}ms")

county_graph.graph_node_opinions(state_name)

plt.show()

