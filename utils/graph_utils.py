import networkx as nx
import matplotlib.pyplot as plt
import time

#-----------------------------------------------------------------------------

class Node:
    def __init__(self, id, name, state, neighbours):
        self.id = id
        self.name = name
        self.state = state
        self.neighbours = neighbours
        self.degree = len(neighbours)
        return
    
#-----------------------------------------------------------------------------

class Graph:
    def __init__(self):
        self.nodes = {}
        self.networkx = nx.Graph()
        return
    
    # Node iterator
    def __iter__(self):
        return iter(self.nodes.values())
    
    # Get number of nodes in the network
    def num_nodes(self):
        return len(self.nodes)
    
    # Add nodes and edges to graph
    def set_topology(self, fipsdict, neighbours):
        start = time.time()

        for fips in fipsdict:
            node = Node(fipsdict[fips]["county"], fipsdict[fips]["state"], neighbours[fips])
            self.nodes[node.id] = node
            self.networkx.add_edges_from([(node.id,neighbour) for neighbour in node.neighbours])

        end = time.time()
        print("Network topology constructed:", round((end-start)*1000), "ms")
        return 

    # Get centrality for each node
    def get_centrality(self):
        """
        # get shortest paths between all nodes in network
        lengths = dict(nx.all_pairs_shortest_path_length(self))
        # compute centrality 
        for source_node in self:
            centrality = 0
            for target_node in self:
                centrality += lengths[source_node.id][target_node.id]
            source_node.centrality = 1 / centrality
        """
        return
    
    # Get superurn ratios for each node, return average ratio
    # Note: get's the player's ratio, not the opponent's
    def get_superurn_ratios(self, player):
        sum = 0
        for node in self:
            r = node.red
            b = node.blue
            for neighbour in node.neighbours:
                r += self.nodes[neighbour].red
                b += self.nodes[neighbour].blue
            if player == "red":
                node.ratio = r / (r+b)
            if player == "blue":
                node.ratio = b / (r+b)
            sum += node.ratio
        avg_ratio = sum / self.nodes()
        return avg_ratio
    
    # Visualize network
    def visualize_graph(self):
        plt.figure()
        nx.draw_spring(self.networkx, with_labels=True)
        plt.show()
        return


