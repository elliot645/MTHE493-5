import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edge(1,2) #creates nodes called 1,2
G.add_edge(2,3)

G.add_edge("A","B") #works with strings
G.add_edge(print,print) #pass in any object, event print function. can pass to itself also

nx.draw_spring(G,with_labels=True) #draw_spring is a type of graph
plt.show()