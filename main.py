from utils.graphutils import Graph, Node, create_county_adjacency_dict, create_voting_data_list
import networkx as nx
import random
from utils.polya_process import polya
import time
import matplotlib.pyplot as plt

state_name = 'NV'
start_year = 2000   # Note: year MUST be a multiple of 4
end_year = 2004

st = time.time()*1000

neighbours = create_county_adjacency_dict("data\countyadj.csv")
t1 = time.time()*1000
print(f"Reading County Adjacency Data: {int(t1-st)}ms")

voting_data = create_voting_data_list("data\countypres_2000-2020.csv")
t2 = time.time()*1000
print(f"Reading County Voting Data: {int(t2-t1)}ms")

# start_profile = get_voting_data(state_name, start_year, voting_data)
# end_profile = get_voting_data(state_name, end_year, voting_data)

county_graph = Graph()

#set up graph
for state in neighbours:
    for county in neighbours[state]:
        population = random.uniform(500,10000)  # population = profile(1)
        red = int(random.uniform(0,population)) # red = profile(2)
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

