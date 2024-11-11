from utils.graphutils import Graph, Node, create_county_adjacency_dict, get_voting_data
import networkx as nx
import random
from utils.polya_process import polya
import time
import matplotlib.pyplot as plt

"""
QUESTION: 
    Superurns are currently formed including counties from other states - do we want this to be the case? 

TO-DO:
    0. Get model running with real data
    1. Create function to calculate accuracy
    2. Create function to run model over various states/years, record accuracy
        i. Run with connected counties
        ii. Run with disconnected counties
"""

def run_model(adj_path, voting_path, state, start_year, end_year):

    valid_years = {2000, 2004, 2008, 2012, 2016, 2020}
    if start_year not in valid_years or end_year not in valid_years:
        print("Data is only available every four years from 2000 to 2020. Please enter different years.")
        return

    st = time.time()*1000 
    # Read adjacency data
    neighbours = create_county_adjacency_dict(adj_path)
    t1 = time.time()*1000
    print(f"Reading County Adjacency Data: {int(t1-st)}ms")
    # Read voting data
    start_data, end_data  = get_voting_data(voting_path, state, start_year, end_year)
    t2 = time.time()*1000
    print(f"Reading County Voting Data: {int(t2-t1)}ms")
    # Create empty graph
    county_graph = Graph()

    # Set up graph for entire country
    # for state in neighbours:
    #     for county in neighbours[state]:
    #         county_name = county[:-10].upper()
    #         red = start_data[county_name]["DEMOCRAT"]
    #         blue = start_data[county_name]["REPUBLICAN"]
    #         population = red + blue
    #         county_graph.add_node(Node(id=county,state=state,red=red,blue=blue,population=population,neighbours = neighbours[state][county]))

    # Set up graph for current state only 
    # for county in neighbours[state]:
    #     county_name = county[:-10].upper()
    #     red = start_data[county_name]["DEMOCRAT"]
    #     blue = start_data[county_name]["REPUBLICAN"]
    #     population = red + blue
    #     county_graph.add_node(Node(id=county, state=state, red=red, blue=blue, population=population, neighbours=neighbours[state][county]))
    
    # t3 = time.time()*1000
    # print(f"Building Graph: {int(t3-t2)}ms")

    # # Plot initial states
    # county_graph.visualize_graph(state)
    # county_graph.graph_node_opinions(state)

    # # Run Polya process
    # t4 = time.time()*1000
    # county_graph, results = polya(county_graph,100,50000,state)
    # t5 = time.time()*1000
    # print(f"Running Polya Process: {int(t5-t4)}ms")

    # # Plot final states
    # county_graph.graph_node_opinions(state)
    # plt.show()

    return 


if __name__ == "__main__":

    # Filepaths for data
    adj_path = "data\countyadj.csv"
    voting_path = "data\countypres.csv"
    
    # CHANGE MODEL PARAMETERS HERE
    state = 'AL'
    start_year = 2000   
    end_year = 2004

    # Run the model for state and years of choice
    run_model(adj_path, voting_path, state, start_year, end_year)

















