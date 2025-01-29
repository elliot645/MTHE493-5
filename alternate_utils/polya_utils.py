import random

"""
Legend:
-------------------
Network:
    i - independent
Memory:
    i - infinite
    f - finite
Replacement:
    c - constant 
    n - node-dependent
    t - time-dependent
    nt - node- and time- dependent
"""

#--------------------------------------------------------------------------

"""
Run indepdent, infinite-memory process with constant delta
Input: graph object, positive integer, positive integer
Output: updated graph object
"""
def polya_i_i_c(graph, delta, timesteps):
    
    for t in range(0,timesteps):
        for node_id, node in graph.nodes.items():
            # variable setup
            r = node.red
            b = node.blue
            if r != "NA" and b != "NA":
                prob_r = r / (r+b)
                # perform draw
                if random.random() < prob_r:
                    choose = 'r'
                else:
                    choose = 'b'
                # reinforcement
                if choose == 'r':
                    node.red += delta
                else:
                    node.blue += delta
            
    return



    

