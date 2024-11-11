from utils.graphutils import Graph, Node, create_county_adjacency_dict, get_voting_data
import networkx as nx
import random
from utils.polya_process import polya
import time
import matplotlib.pyplot as plt

# CHANGE MODEL PARAMETERS HERE
state_name = 'NV'
start_year = 2000   # Note: year MUST be a multiple of 4
end_year = 2004
adj_path = "data\countyadj.csv"
voting_path = "data\countypres.csv"

st = time.time()*1000 

neighbours = create_county_adjacency_dict(adj_path)
t1 = time.time()*1000
print(f"Reading County Adjacency Data: {int(t1-st)}ms")

voting_data = get_voting_data(voting_path, state_name, start_year, end_year)
start_data = voting_data[0]
end_data = voting_data[1]
t2 = time.time()*1000
print(f"Reading County Voting Data: {int(t2-t1)}ms")

county_graph = Graph()

#set up graph
for state in neighbours:
    for county in neighbours[state]:
        population = random.uniform(500,10000)  
        red = int(random.uniform(0,population))
        blue = population - red
        county_graph.add_node(Node(id=county,state=state,red=red,blue=blue,population=population,neighbours = neighbours[state][county]))

t3 = time.time()*1000
print(f"Building Graph: {int(t3-t2)}ms")

county_graph.visualize_graph(state_name)
county_graph.graph_node_opinions(state_name)

t4 = time.time()*1000
#Feed into polya model
county_graph, results = polya(county_graph,100,50000,state_name)
t5 = time.time()*1000
print(f"Running Polya Process: {int(t5-t4)}ms")

county_graph.graph_node_opinions(state_name)

plt.show()

