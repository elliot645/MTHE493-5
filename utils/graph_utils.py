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
            node = Node(fips, fipsdict[fips]["county"], fipsdict[fips]["state"], neighbours[fips])
            self.nodes[node.id] = node
            self.networkx.add_edges_from([(node.id,neighbour) for neighbour in node.neighbours])

        end = time.time()
        print("Network topology constructed:", round((end-start)*1000), "ms")
        return 

    # Set node centrality
    def set_centrality(self, centrality):
        for node in self:
            if len(str(node.id)) == 4:
                id_string = "0" + str(node.id)
            else:
                id_string = str(node.id)
            if id_string in centrality:
                node.centrality = centrality[id_string]
            else:
                node.centrality = 0.000001
                print("No centrality for", node.id, node.name, node.state)
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
    def visualize_graph(self):
        plt.figure()
        nx.draw_spring(self.networkx, with_labels=True)
        plt.show()
        return


