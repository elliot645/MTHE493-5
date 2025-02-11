import random
import numpy as np
import graphutils

# Updated polya function with additional functionality for aging, new entries, and death
def polya(graph, n, state_filter=None, steps_per_year=1):
    perc_death = graphutils.death_data_array_generator()
    if state_filter is not None:
        results = {node_id: [] for node_id in graph.nodes if graph.nodes[node_id].state == state_filter}
    else:
        results = {node_id: [] for node_id in graph.nodes}

    for i in range(n):
        for node_id, node in graph.nodes.items():
            if state_filter is not None and node.state != state_filter:
                continue

            r = sum(node.red)
            b = sum(node.blue)
            p = r + b
            for neighbour in node.neighbours:
                r += sum(graph.nodes[neighbour].red)
                b += sum(graph.nodes[neighbour].blue)
            t = r + b

            delta = 12/1000 * p * 1/steps_per_year # 12 births/year per 1000 people in U.S.
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
            

            #reinforcement_parameter = population[node.state][node.county]/1000 * brths/k/yr * 1/steps_per_year
            #assuming 12 births/1000 ppl per year (can develop more)

                #Get births per time period per capita yearly, use to calculate num births, maybe some randomization. Use node data to index data frame. Then use that reinforcement
            # Update node
            if choose == 'r':
                node.red[18] += delta
            else:
                node.blue[18] += delta

            # Save data
            data = {'choose': choose, 'total': sum(node.red) + sum(node.blue), 'red ratio': sum(node.red) / (sum(node.red) + sum(node.blue))}
            results[node_id].append(data)

            # Death process
            for age in range(len(node.red)):
                if perc_death is not None:
                    death_prob = perc_death[age] / steps_per_year
                    num_red_deaths = np.random.binomial(node.red[age], death_prob)
                    num_blue_deaths = np.random.binomial(node.blue[age], death_prob)
                    node.red[age] -= num_red_deaths
                    node.blue[age] -= num_blue_deaths

        # Ageing process for each year
        if (i + 1) % steps_per_year == 0:
            for node in graph.nodes.values():
                # Shift the age distribution to the right
                node.red = [0] + node.red[:-1]
                node.blue = [0] + node.blue[:-1]


    return graph, results

