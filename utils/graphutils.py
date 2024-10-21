import pandas as pd

class Graph:
    def __init__(self,adj_matrix=None,red_dict={},blue_dict={},population_dict={},lat_dict={},long_dict={},reinforcement_dict={}):
        self.red = red_dict
        self.blue = blue_dict
        self.population = population_dict
        self.lat = lat_dict
        self.long = long_dict
        self.reinforcement_paramter = reinforcement_dict

        #Need a way to initialize neighbours using adj_matrix. Ideally it's a matrix, not a list.
        self.neighbours = adj_matrix
        return

    def add_node(self,node,neighbours=[]):
        self.red[node.id] = node.red
        self.blue[node.id] = node.blue
        self.population[node.id] = node.population
        self.lat[node.id] = node.lat
        self.long[node.id] = node.long
        self.neighbours[node.id] = neighbours
        self.reinforcement_parameter[node.id] = node.reinforcement_parameter
        return
    
    def add_edge(self,node1,node2):
        self.neighbours[node1.id].append(node2.id)
        self.neighbours[node2.id].append(node1.id) 

class Node:
    def __init__(self,id,population=None,red=None,blue=None,lat=None,long=None,reinforcement_parameter=1):
        self.id = id
        self.population = population
        self.red = red
        self.blue = blue
        self.lat = lat
        self.long = long
        self.reinforcement_parameter = reinforcement_parameter
        return
