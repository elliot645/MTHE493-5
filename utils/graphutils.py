import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
#import immigration
from . import map_visualization

class Graph:
    def __init__(self):
        self.nodes = {}
        self.networkx = nx.Graph()
        return

    #Add a new node (or replace an existing node with the same ID)
    def add_node(self, node):
        self.nodes[node.id] = node

        #Add node and its edges to the networkX graph
        self.networkx.add_edges_from([(node.id,neighbour) for neighbour in node.neighbours])
    
    def add_edge(self, node_id1, node_id2):
        if node_id1 not in self.nodes.keys or node_id2 not in self.nodes.keys:
            return
        self.node[node_id1].neighbours.add(node_id2)
        self.node[node_id2].neighbours.add(node_id1)
 
        #Add edge to networkx graph
        self.networkx.add_edge(node_id1,node_id2)

    def visualize_graph(self,state=None):
        #todo: labels below nodes, grey/translucent edges, add colors or gradient to denote opinions
        #Ideally, we can get node coordiantes to visualize them as they look on a map
        # pos[center_node] = np.array([0, 0])  # manually specify node position
        # nx.draw(G, pos, with_labels=True)
        plt.figure()
        if state is not None:
            G = nx.subgraph(self.networkx,[county for county in self.nodes if self.nodes[county].state == state])
            nx.draw_spring(G,with_labels=True)

        else:
            nx.draw_spring(self.networkx,with_labels=True)
        return
    
    def visualize_map(self,states):
        map_visualization.visualize_state_opinions(states,self)
        return

    
    def graph_node_opinions(self,state=None,title=None):
        plt.figure()
        if state is None:
            nodes = self.nodes
        else:
            nodes = [county for county in self.nodes if self.nodes[county].state == state]
        red_counts = []
        blue_counts = []
        counties = []

        for node in nodes:
            counties.append(node)
            red_counts.append(self.nodes[node].red)
            blue_counts.append(self.nodes[node].blue)

        # Define bar width and positions
        bar_width = 0.35
        x = np.arange(len(counties))  # X-axis positions for counties
      
        # Plot bars
        plt.bar(x - bar_width / 2, red_counts, width=bar_width, color='red', label='Red Votes')
        plt.bar(x + bar_width / 2, blue_counts, width=bar_width, color='blue', label='Blue Votes')

        # Labeling
        plt.xlabel('County')
        plt.ylabel('Number of Votes')
        if title is None:
            if state is not None:
                plt.title(f'{state}: Votes by County and Party')
            else:
                plt.title('Votes by County and Party')
        else:
            plt.title(title)
        plt.title('Votes by County and Party')
        plt.xticks(x, counties, rotation=45, ha='right')
        plt.legend()

        # Display the plot
        plt.tight_layout()
        return
        
class Node:
    def __init__(self,id,county,state,population=None,red=None,blue=None,lat=None,long=None,reinforcement_parameter=1,neighbours = ()):
        self.id = id #FIPS ID
        self.county = county
        self.state = state
        self.population = population #will be a list for every age
        self.red = red if red else [0] * 100
        self.blue = blue if blue else [0] * 100
        self.lat = lat
        self.long = long
        self.reinforcement_parameter = reinforcement_parameter
        self.neighbours = neighbours
        return

def create_county_adjacency_dict(file_path):
   
    adjacency_matrix = pd.read_csv(file_path, index_col=0)
    
    county_adjacency_dict = {}

    for county in adjacency_matrix.index:
        state = county[-2:] 
        if state not in county_adjacency_dict:
            county_adjacency_dict[state] = {}
        
        adjacent_counties = set(adjacency_matrix.loc[county][adjacency_matrix.loc[county] == 1].index.tolist())
        county_adjacency_dict[state][county] = adjacent_counties

    return county_adjacency_dict

def create_voting_data_list(file_path):
    # Read csv into dataframe
    df = pd.read_csv(file_path)

    # Convert into list of dicts like [{col:val, ..., col:val}, ... , {col:val, ... , col:val}]
    voting_data = df.to_dict(orient="records")

    return voting_data

#FOR JORDAN
def update_reinforcement_using_daily_birthds(self):
    #Calculate the number of births for the day
    #Update self.reinforcement_parameter to this value
    #With this function, the polya process will call this function at every time step for every node
    #The reinforcement parameter will be updated at every time step
    pass

def get_voting_data(state, year, voting_data):
    pass

    """
    ASSUMPTIONS:
        1. County population = total county votes?
        2. What to do about other parties?

    """

def death_data_array_generator():
    df = pd.read_csv("death_data.csv")

  
    df = df[['age', 'death_probm', 'death_probf']]


    df = df.sort_values('age').reset_index(drop=True)

    death_prob_array = np.zeros(120)  
    #death prob per year of living is average of male and female at given age
    for _, row in df.iterrows():
        death_prob_array[int(row['age'])] = (row['death_probm'] + row['death_probf'])/2

    return death_prob_array