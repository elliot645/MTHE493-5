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
                r += graph.nodes[neighbour].red/10 #/10 so they are not as prevelant in the super node
                b += graph.nodes[neighbour].blue/10
            t = r + b

            delta = 12/1000 * (r+b) /10  # 12 births/year per 1000 people in U.S.
            y = random.random() #rand in [0,1]
            # Get the decimal value of delta
            decimal_value = delta - int(delta)
            # Check and round based on the comparison
            delta = int(delta) + 1 if decimal_value > y else int(delta) #round delta based on randomization 

            prob_r = r / t

            if random.random() < prob_r:
                choose = 'r'
            else:
                choose = 'b'

            if choose == 'r':
                node.red += delta
            else:
                node.blue += delta

            #save data
            data = {'choose':choose,
                    'total':node.red + node.blue,
                    'red ratio': node.red/(node.red + node.blue)
            }
            results[node_id].append(data)
    return graph, results
