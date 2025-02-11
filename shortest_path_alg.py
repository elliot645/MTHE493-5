
from utils.graphutils import Graph, Node, create_county_adjacency_dict_fips, create_voting_data_list
import pandas as pd
import heapq
import matplotlib.pyplot as plt
import csv
import json

#-----------------------------------------------------------------------------

def dijkstra(graph, start_id):
    # Priority queue for the minimum distance
    pq = []
    heapq.heappush(pq, (0, start_id))  # (distance, node_id)
    
    # Dictionary to store shortest distances
    shortest_distances = {node_id: float('inf') for node_id in graph.nodes}
    shortest_distances[start_id] = 0
    
    # Dictionary to store the previous node in the path
    previous_nodes = {node_id: None for node_id in graph.nodes}
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # If we already found a shorter path, skip processing
        if current_distance > shortest_distances[current_node]:
            continue
        
        # Iterate over neighbors and relax edges
        for neighbour in graph.nodes[current_node].neighbours:
            distance = current_distance + 1
            
            if distance < shortest_distances[neighbour]:
                shortest_distances[neighbour] = distance
                previous_nodes[neighbour] = current_node
                heapq.heappush(pq, (distance, neighbour))
    
    return shortest_distances #, previous_nodes


#-------------------------------------

def test_dijkstra():
    graph = Graph()

    a = Node('a','X','X')
    b = Node('b','X','X')
    c = Node('c','X','X')
    d = Node('d','X','X')
    e = Node('e','X','X')
    f = Node('f','X','X')

    a.neighbours = {'b','d'}
    b.neighbours = {'a','c'}
    c.neighbours = {'b','d'}
    d.neighbours = {'a','c','e'}
    e.neighbours = {'d','f'}
    f.neighbours = {'e'}

    nodes = [a,b,c,d,e,f]

    for n in nodes:
        graph.add_node(n)

    #graph.visualize_graph()
    #plt.show()

    print(graph.nodes)

    print(dijkstra(graph,'a'))


#------------------------------------------------------

#Get the shortest path dict for the country or just a state
# filtered_state is a fips (e.g. to '12' to filter on Florida) 
def get_shortest_path_dict(filtered_state=None): 

    #Get County Adjacency Matrix
    neighbours = create_county_adjacency_dict_fips("data\countyadj.csv")

    #Get FIPS (IDs) data for every county
    county_fips = pd.read_csv('data/fips.csv',dtype=str, encoding='utf-8').set_index(["STATE","COUNTY"]).drop_duplicates()

    #Define Graph variable
    county_graph = Graph()

    #Initialize Graph 
    for county_id in neighbours:

        #Filter on a state
        if filtered_state is not None and county_id[:2] != filtered_state:
            continue

        county_name = county_fips.loc[(county_id[:2],county_id[2:])]['CTYNAME']
        state_name = county_fips.loc[(county_id[:2],county_id[2:])]['STNAME']  
        county_graph.add_node(Node(
                id=county_id,
                county=county_name,
                state=state_name,                    
                neighbours = [n for n in neighbours[county_id] if n[:2] == filtered_state] if filtered_state is not None else neighbours[county_id]
        ))

    counties = {}

    for id in county_graph.nodes:
        counties[id] = dijkstra(county_graph,id)

    return counties

#--------------------------------------------------------------

def get_centrality_values(filtered_state=None):
    shortest_paths = get_shortest_path_dict(filtered_state)

    centrality_vals = {}

    #Centrality equation
    def centrality(node_id):
        total = sum(shortest_paths[node_id].values())
        return 1/total
    
    neighbours = create_county_adjacency_dict_fips("data\countyadj.csv")
    for county_id in [n for n in neighbours if n[:2] == filtered_state]:
        centrality_vals[county_id] = centrality(county_id)

    return centrality_vals

#--------------------------------------------------------------

def dict_to_csv(counties_dict,csv_name):
    df = pd.DataFrame.from_dict(counties_dict, orient="index")
    df.to_csv(f'{csv_name}.csv')

def csv_to_dict(csv_name):
    #Read the csv, keeping values as string to preserve leading zeros
    df = pd.read_csv('dijkstra USA.csv', dtype=str)
    #Set the first column as the index
    df.set_index(df.columns[0], inplace=True)

    #Convert the values from strings to ints
    df = df.apply(pd.to_numeric)

    #Create dict
    return df.to_dict(orient="index")

def dict_to_json(dict,json_name):
    with open(f'{json_name}.json', 'w') as json_file:
        json.dump(dict, json_file)

def json_to_dict(json_name):
    with open(f'{json_name}.json', 'r') as json_file:
        return json.load(json_file)

#----------------------------------------

"""
Note that the dijkstra algorithm takes a while, so 
it's best to run the get_centrality_values() function once, and then convert to a json

Then, in the main function, use the json_to_dict function to get a dictionary of all the
centrality values by county.

Example:

1. Run this once
fl_centrality_values = get_centrality_values('12')
dict_to_json(fl_centrality_values,'fl_centrality_values')

2. Run this in main
fl_centrality_values = json_to_dict('fl_centrality_values')
.
.
.
And then initialize nodes (something along the lines of below)
Graph[nodeid].centrality = fl_centrality_values[node_id]
"""

#Example Test Code

# x = get_centrality_values('12')
# print(len(x))
# dict_to_json(x,'fl_centrality_values')