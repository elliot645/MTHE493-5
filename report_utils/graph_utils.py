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
    
    # use with json files
    def set_state_topology(self, state, fipsdict, adjdict):
        for fips in fipsdict[state]:
            node = Node(fips, fipsdict[state][fips], state, adjdict[state][fips])
            self.nodes[fips] = node
            self.networkx.add_edges_from([(fips, neighbour) for neighbour in node.neighbours])
        return
    
    # use with json files
    def set_state_centrality(self, state, centralitydict):
        for node in self:
            node.centrality = centralitydict[state][node.id]
        return

    # Update ratios and superurn ratios for each node
    #   - return's average urn ratio weighted by population
    #   - ratios calculated based on specified player
    def update_superurn_ratios(self, player):
        sum = 0
        total_pop = 0
        for node in self:
            r = node.red
            b = node.blue
            # update node's ratio
            if player == "red":
                node.ratio = r / (r+b)
            if player == "blue":
                node.ratio = b / (r+b)
            # update node's superurn ratio
            for neighbour in node.neighbours:
                r += self.nodes[neighbour].red
                b += self.nodes[neighbour].blue
            if player == "red":
                node.suratio = r / (r+b)
            if player == "blue":
                node.suratio = b / (r+b)
            # calculate average ratio weighted by population
            sum += node.pop*node.ratio
            total_pop += node.pop
        avg_ratio = sum / total_pop
        return avg_ratio
    
    # Visualize network
    def visualize_graph(self, state):
        plt.figure()
        nx.draw_spring(self.networkx, with_labels=True)
        plt.title(state)
        plt.show()
        return


