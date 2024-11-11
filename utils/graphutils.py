import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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
    def __init__(self,id,state,population=None,red=None,blue=None,lat=None,long=None,reinforcement_parameter=1,neighbours = ()):
        self.id = id
        self.state = state
        self.population = population
        self.red = red
        self.blue = blue
        self.lat = lat
        self.long = long
        self.reinforcement_parameter = reinforcement_parameter
        self.neighbours = neighbours
        return

def create_county_adjacency_dict(file_path):
   
    adjacency_matrix = pd.read_csv(file_path, index_col=0)
    
    county_adjacency_dict = {}

    for county in adjacency_matrix.index:
        state = county.split()[-1] 
        if state not in county_adjacency_dict:
            county_adjacency_dict[state] = {}
        
        adjacent_counties = set(adjacency_matrix.loc[county][adjacency_matrix.loc[county] == 1].index.tolist())
        county_adjacency_dict[state][county] = adjacent_counties

    return county_adjacency_dict


def get_voting_data(file_path, state, start_year, end_year):

    # Read csv into dataframe
    df = pd.read_csv(file_path)
    df = df[df["state_po"] == state]

    # Subset dataframe to rows of interest
    start_df = df[df["year"] == start_year]
    end_df = df[df["year"] == end_year]

    # Convert into list of dicts 
    start_data = start_df.to_dict(orient="records")
    end_data = end_df.to_dict(orient="records")

    # Dict to hold data for county-year
    start_dict = {
        "state" : state,
        "year" : start_year
    }

    end_dict = {
        "state" : state,
        "year" : end_year
    }

    # Loop through dataset, add a dict of votes for each county
    for row in start_data:
        county = row["county_name"]
        party = row["party"]
        votes = row["candidatevotes"]

        # If county not in state_dict, add it as key with empty dict as value
        if county not in start_dict.keys():
            start_dict[county] = {"total_votes" : row["totalvotes"]}

        # Add party and votes to county dict
        start_dict[county][party] = votes 

    # Repeat for end year
    for row in end_data:
        county = row["county_name"]
        party = row["party"]
        votes = row["candidatevotes"]

        if county not in end_dict.keys():
            end_dict[county] = {"total_votes" : row["totalvotes"]}

        end_dict[county][party] = votes 

    return start_dict, end_dict 



    
