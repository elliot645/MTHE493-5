from utils.graphutils import Graph, Node, create_county_adjacency_dict, create_voting_data_list
import networkx as nx
import random
from utils.polya_process import polya
import time
import matplotlib.pyplot as plt
import utils.population
import pandas as pd

#Set Initial Values
state_name = 'NV'
start_year = 2000   # Note: year MUST be a multiple of 4
end_year = 2004

st = time.time()*1000

#Get County Adjacency Matrix
neighbours = create_county_adjacency_dict("data\countyadj.csv")
#populations = population.get_population_data(state=state_name,year=start_year)

t1 = time.time()*1000
print(f"Reading County Adjacency Data: {int(t1-st)}ms")

#Get voting data
voting_data = create_voting_data_list("data\countypres_2000-2020.csv")
t2 = time.time()*1000
print(f"Reading County Voting Data: {int(t2-t1)}ms")

#Get FIPS (IDs) data for every county
county_fips = pd.read_csv('data/fips.csv',dtype=str, encoding='latin1').set_index(["STNAME","CTYNAME"]).drop_duplicates()

print(county_fips.loc['New Mexico'])

#start_profile = get_voting_data(state_name, start_year, voting_data)
#end_profile = get_voting_data(state_name, end_year, voting_data)

#Get full state names based on abberviations (used in adjacency matrix)
state_abbrevs = pd.read_csv('data/state_abbreviations.csv',dtype=str, encoding='latin-1').set_index("state_abbrev").drop_duplicates()

#Define Graph variable
county_graph = Graph()

#Initialized graph: 
# - set population, red, blue in each node
# - connect nodes using adjacency matrix
for state in neighbours:
    for county in neighbours[state]:
        county_name = county[:-3] # remove the state abbreviation at the end (e.g. "New York NY" becomes "New York")
        state_name = state_abbrevs.loc[state]['state']
        print(f"{state_name} {county_name}")

        population = random.uniform(500,10000)  #Eventually, will be = populations[state][county]
        red = int(random.uniform(0,population)) # red = profile(2)
        blue = population - red
        county_graph.add_node(Node(
            id=county_fips.loc[(state_name,county_name)]['STATE'] + county_fips.loc[(state_name,county_name)]['COUNTY'],
            county=county_name,
            state=state_abbrevs.loc[state]['state'],
            red=red,
            blue=blue,
            population=population,
            neighbours = {n[:-3] for n in neighbours[state][county]},
            reinforcement_parameter=10 #This is the initial reinforcement parameter. Will be overwritten once we have the birth function going.
            ))
        
t3 = time.time()*1000
print(f"Building Graph: {int(t3-t2)}ms")

#Display Graph Before Simulation
county_graph.visualize_graph(state_name)
county_graph.graph_node_opinions(state_name)

#Run Simulation
t4 = time.time()*1000
county_graph, results = polya(county_graph,1000,state_name)
t5 = time.time()*1000
print(f"Running Polya Process: {int(t5-t4)}ms")

#Display node opinions after simulation
county_graph.graph_node_opinions(state_name)

plt.show()

