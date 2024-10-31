import random

def polya(graph, reinforce, n,state_filter=None):
    if state_filter is not None:
        results = {node_id: [] for node_id in graph.nodes if graph.nodes[node_id].state == state_filter}
    else:
        results = {node_id: [] for node_id in graph.nodes}

    for i in range(0,n):
        for node_id,node in graph.nodes.items():
            if state_filter is not None:
                if node.state != state_filter:
                    continue #skip over nodes that aren't in the state we are running the polya process on

            r = node.red 
            b = node.blue
            for neighbour in node.neighbours:
                r += graph.nodes[neighbour].red
                b += graph.nodes[neighbour].blue
            t = r + b
            prob_r = r/t

            if random.random() < prob_r:
                choose = 'r'
            else:
                choose = 'b'

            #update node
            if choose == 'r':
                node.red += reinforce
            else:
                node.blue += reinforce

            #save data
            data = {'choose':choose,
                    'total':node.red + node.blue,
                    'red ratio': node.red/(node.red + node.blue)
            }
            results[node_id].append(data)
    return graph, results

def polya_reinforce_by_node(graph):
   results = []
   for node in graph.nodes:
       r = node.red 
       b = node.blue

       for neighbour in node.neighbours:
           t += (neighbour.red + neighbour.blue)
           r += neighbour.red
           b += neighbour.blue

           t = r + b
           prob_r = r/t

       if random.random() < prob_r:
           choose = 'r'
       else:
           choose = 'b'

       if choose == 'r':
           node.r += node.reinforcement_parameter
       else:
           node.b += node.reinforcement_parameter

       data = [choose,node.red + node.blue + node.reinforcement_parameter,node.red/(node.red + node.blue + node.reinforcement_parameter)]
       results.append(data) 
   return      

#each node has a list of its neighbours from adjacency matrix
