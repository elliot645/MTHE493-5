import random

def polya(graph, n,state_filter=None):
    #State filter is used to only run the process on a specific state, making it faster
    if state_filter is not None:
        results = {node_id: [] for node_id in graph.nodes if graph.nodes[node_id].state == state_filter}
    else:
        results = {node_id: [] for node_id in graph.nodes}

    #Run the process n times
    for i in range(0,n):
        for node_id,node in graph.nodes.items():
            if state_filter is not None:
                if node.state != state_filter:
                    continue #skip over nodes that aren't in the state we are running the polya process on
            
            #Select ball from super urn
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

            #Add balls of the chosen color to the super urn
            if choose == 'r':
                node.red += node.reinforcement_parameter
            else:
                node.blue += node.reinforcement_parameter

            #save data
            data = {'choose':choose,
                    'total':node.red + node.blue,
                    'red ratio': node.red/(node.red + node.blue)
            }
            results[node_id].append(data)
    return graph, results
