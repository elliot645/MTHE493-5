from utils.graphutils import Graph, Node, create_county_adjacency_dict_fips, create_voting_data_list
import networkx as nx
import random
from utils.polya_process import polya
import time
import matplotlib.pyplot as plt
import utils.population
import pandas as pd
from utils.voting_utils import *

#Set Initial Values
state_to_graph = 'Florida'
start_year = 2000   # Note: year MUST be a multiple of 4
end_year = 2004

#Get County Adjacency Matrix
neighbours = create_county_adjacency_dict_fips("data\countyadj.csv")

#populations = population.get_population_data(state=state_name,year=start_year)

#Get FIPS (IDs) data for every county
county_fips = pd.read_csv('data/fips.csv',dtype=str, encoding='utf-8').set_index(["STATE","COUNTY"]).drop_duplicates()

#Get voting data
voting_path = "data\countypres.csv"
voting_data = get_votes(pd.read_csv(voting_path), 2020)

#centrality

#Define Graph variable
county_graph = Graph()

# Initialize graph: 
# - set population, red, blue in each node
# - connect nodes using adjacency matrix
for county_id in neighbours:
    county_name = county_fips.loc[(county_id[:2],county_id[2:])]['CTYNAME']
    state_name = county_fips.loc[(county_id[:2],county_id[2:])]['STNAME']
    #print(f"{state_name} {county_name}")

    population = random.uniform(500,10000)  #Eventually, will be = populations[state][county]
    red = voting_data[county_id]['red']
    blue = voting_data[county_id]['blue']
    county_graph.add_node(Node(
            id=county_id,
            county=county_name,
            state=state_name,
            red=red,
            blue=blue,
            population=population,
            neighbours = neighbours[county_id],
            reinforcement_parameter=10 #This is the initial reinforcement parameter. Will be overwritten once we have the birth function going.
    ))


county_graph.visualize_map(title_size=21,legend_size=10,annotation_size=9,image_size=13)
county_graph.graph_node_opinions("Florida")

county_graph, results = polya(county_graph,1500)

county_graph.visualize_map(title_size=21,legend_size=10,annotation_size=9,image_size=13)
county_graph.graph_node_opinions("Florida")

# plt.savefig('pictures/graph/initial.png')
# plt.savefig('image_1.png')


plt.show()
# county_graph.graph_node_opinions("Florida")
# plt.savefig('pictures/graph/initial.png')

# for i in range(2,15):
#     county_graph, results = polya(county_graph,40)
#     county_graph.visualize_map(title_size=21,legend_size=10,annotation_size=9,image_size=13)
#     plt.savefig(f'image_{i}.png')
#     # county_graph.graph_node_opinions("Florida")
#     # plt.savefig('foo4.png')

# #plt.show()