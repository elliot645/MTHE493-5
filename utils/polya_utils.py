from utils.graph_utils import *
import random, math


def binary_entropy(p):
    if 0 < p and p < 1:
        return p*math.log2(p) + (1-p)*math.log2(1-p)
    else:
        return 0


#--------------------------------------------------------------------------
# Classical Polya Process
#--------------------------------------------------------------------------

# run polya process for given R, B, timesteps, and delta
def classic_polya(r, b, timesteps, delta):
    for t in range(0, timesteps):
        prob_red = r/(r+b)
        if random.random() < prob_red:
            r += delta
        else:
            b += delta
    ratio = r/(r+b)
    return ratio

#--------------------------------------------------------------------------
# Curing via Reinforcement
#--------------------------------------------------------------------------

# uniform vs. uniform
def uniform_vdelta(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    # calculate initial infection rate
    results = {}
    results[0] = network.update_superurn_ratios(player)
    # begin polya process
    for t in range(1, timesteps+1):
        # perform draws across all nodes
        for node in network:
            # calculate delta values
            delta_red = rbudget / network.num_nodes()
            delta_blue = bbudget / network.num_nodes()
            # get superurn ratios
            if player == "red":
                prob_red = node.suratio
            if player == "blue":
                prob_red = 1 - node.suratio
            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue
        # calculate infection rate across network
        results[t] = network.update_superurn_ratios(player)
    return results

# population-weighted vs. uniform
def pop_vdelta(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    # calculate initial infection rate
    results = {}
    results[0] = network.update_superurn_ratios(player)
    # get total population
    total_pop = 0
    for node in network:
        total_pop += node.pop
    # begin polya process
    for t in range(1, timesteps+1):
        for node in network:
            # calculate delta values and superurn ratios
            if player == "red":
                delta_red = (node.pop/total_pop)*rbudget
                delta_blue = bbudget / network.num_nodes()
                prob_red = node.suratio
            if player == "blue":
                delta_red = rbudget / network.num_nodes()
                delta_blue = (node.pop/total_pop)*bbudget
                prob_red = 1 - node.suratio
            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue
        # calculate infection rate across network
        results[t] = network.update_superurn_ratios(player)
    return results

# centrality-infection-weighted vs. uniform
def ci_vdelta(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    # calculate initial infection rate
    results = {}
    results[0] = network.update_superurn_ratios(player)
    for t in range(1, timesteps+1):
        # get CIR denominator for this timestep
        denom = 0
        for node in network:
            denom += node.degree*node.centrality*(1-node.ratio)
        for node in network:
            # calculate delta values
            if player == "red":
                delta_red = (rbudget*node.degree*node.centrality*(1-node.ratio)) / denom
                delta_blue = bbudget / network.num_nodes()
                prob_red = node.suratio
            if player == "blue":
                delta_red = rbudget / network.num_nodes()
                delta_blue = (bbudget*node.degree*node.centrality*(1-node.ratio)) / denom
                prob_red = 1 - node.suratio
            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue
        # calculate infection rate
        results[t] = network.update_superurn_ratios(player)
    return results
            
# population- and centrality-infection-weighted vs. uniform
def pop_ci_vdelta(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    # calculate initial infection rate
    results = {}
    results[0] = network.update_superurn_ratios(player)
    for t in range(1, timesteps+1):
        # get CIR denominator for this timestep
        denom = 0
        for node in network:
            denom += node.pop*node.degree*node.centrality*(1-node.ratio)
        for node in network:
            # calculate delta values
            if player == "red":
                delta_red = ((node.pop*node.degree*node.centrality*(1-node.ratio))/denom)*rbudget
                delta_blue = bbudget / network.num_nodes()
                prob_red = node.suratio
            if player == "blue":
                delta_red = rbudget / network.num_nodes()
                delta_blue = ((node.pop*node.degree*node.centrality*(1-node.ratio))/denom)*bbudget
                prob_red = 1 - node.suratio
            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue
        # calculate infection rate
        results[t] = network.update_superurn_ratios(player)
    return results

#--------------------------------------------------------------------------
# Curing via Injection
#--------------------------------------------------------------------------

# # uniform vs. uniform
# def uniform_injection_strategy(network, params):
#     # unbox params
#     player = params["player"]
#     rbudget = params["rbudget"]
#     bbudget = params["bbudget"]
#     timesteps = params["timesteps"]
#     # calculate initial ratios
#     results = {}
#     results[0] = network.update_superurn_ratios()
#     # begin polya process
#     for t in range(timesteps):
#         if player == "red":
#             total_budget = rbudget
#             passive_player = "blue"
#         elif player == "blue":
#             total_budget = bbudget
#             passive_player = "red"
#         else: 
#             raise ValueError("Player should be red or blue")
#         budget_per_node = total_budget / network.total_nodes
#         for node in network.counties:
#             urn = network.urns[node]
#             neighbours = network.adjacency_map[node]
#             for _ in range(int(budget_per_node)):
#                 if neighbours:
#                     choose_random_neighbour = random.choice(neighbours)
#                     draw_ball = random.choice([player, passive_player])
#                     network.populations[node][draw_ball]-=1
#                     network.populations[choose_random_neighbour][draw_ball] +=1
#         average_ratio = network.ratio
#         results[t] = average_ratio
#     return results

# Uniform vs. uniform 
def uniform_vinjection(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    delta = params["delta"]
    # calculate initial infection rate
    results = {}
    results[0] = network.update_superurn_ratios(player)
    # begin polya process
    for t in range(1, timesteps+1):
        # perform injection
        for node in network:
            node.red += rbudget / network.num_nodes()
            node.blue += bbudget / network.num_nodes()
        # update superurn ratios
        network.update_superurn_ratios(player)
        # perform polya process
        for node in network:
            # calculate draw probability
            if player == "red":
                prob_red = node.suratio
            if player == "blue":
                prob_red = 1 - node.suratio
            # perform draw
            if random.random() < prob_red:
                node.red += delta
            else:
                node.blue += delta
        # calculate average urn ratio at this timestep
        results[t] = network.update_superurn_ratios(player)
    return results

# population-weighted vs. uniform
def pop_vinjection(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    delta = params['delta']
    # calculate initial infection rate
    results = {}
    results[0] = network.update_superurn_ratios(player)
    # get total population
    total_pop = 0
    for node in network:
        total_pop += node.pop
    # begin polya process
    for t in range(1, timesteps+1):
        # perform injection
        for node in network:
            if player == "red":
                node.red += (node.pop/total_pop)*rbudget
                node.blue += bbudget / network.num_nodes()
            if player == "blue":
                node.red += rbudget / network.num_nodes()
                node.blue += (node.pop/total_pop)*bbudget
        # update urn and superurn ratios
        network.update_superurn_ratios(player)
        # perform polya process
        for node in network:
            # calculate draw probability
            if player == "red":
                prob_red = node.suratio
            if player == "blue":
                prob_red = 1 - node.suratio
            # perform draw
            if random.random() < prob_red:
                node.red += delta 
            else:
                node.blue += delta
        # calculate average urn ratio at this timestep
        results[t] = network.update_superurn_ratios(player)
    return results

# CIR-weighted vs. uniform injection
def ci_vinjection(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    delta = params['delta']
    # calculate initial ratios
    results = {}
    results[0] = network.update_superurn_ratios(player)
    for t in range(1, timesteps+1):
        # get CIR denominator for this timestep
        denom = 0
        for node in network:
            denom += node.degree*node.centrality*(1-node.ratio)
        # perform injection
        for node in network:
            if player == "red":
                node.red += (rbudget*node.degree*node.centrality*(1-node.ratio)) / denom
                node.blue += bbudget / network.num_nodes()
            if player == "blue":    
                node.red += rbudget / network.num_nodes()
                node.blue += (bbudget*node.degree*node.centrality*(1-node.ratio)) / denom
        # update superurn ratios
        network.update_superurn_ratios(player)
        # perform polya process 
        for node in network:
            # calculate draw probability
            if player == "red":
                prob_red = node.suratio
            if player == "blue":
                prob_red = 1 - node.suratio 
            # perform draw
            if random.random() < prob_red:
                node.red += delta 
            else:
                node.blue += delta
        # calculate average urn ratio at this timestep
        results[t] = network.update_superurn_ratios(player)
    return results

# population- and CIR-weighted vs. uniform
def pop_ci_vinjection(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    delta = params['delta']
    # calculate initial ratios
    results = {}
    results[0] = network.update_superurn_ratios(player)
    # calculate total population
    total_pop = 0
    for node in network:
        total_pop += node.pop
    # begin polya process
    for t in range(1, timesteps+1):
        # get pop-CIR denominator for this timestep
        denom = 0
        for node in network:
            denom += node.pop*node.degree*node.centrality*(1-node.ratio)
        # perform injection at this timestep
        for node in network:
            if player == "red":
                node.red += (rbudget*node.pop*node.degree*node.centrality*(1-node.ratio)) / denom
                node.blue += bbudget / network.num_nodes()
            if player == "blue":    
                node.red += rbudget / network.num_nodes()
                node.blue += (bbudget*node.pop*node.degree*node.centrality*(1-node.ratio)) / denom
        # update superurn ratios
        network.update_superurn_ratios(player)
        # perform polya at this timestep 
        for node in network:
            # calculate draw probability
            if player == "red":
                prob_red = node.suratio
            if player == "blue":
                prob_red = 1 - node.suratio 
            # perform draw
            if random.random() < prob_red:
                node.red += delta 
            else:
                node.blue += delta
        # calculate average urn ratio at this timestep
        results[t] = network.update_superurn_ratios(player)
    return results
        
# binary entropy (of superurn?) vs. uniform 
def besu_vinjection(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    delta = params['delta']
    # calculate initial infection rate
    results = {}
    results[0] = network.update_superurn_ratios(player)
    for t in range(1, timesteps+1):
        # get BE denominator at this timestep 
        denom = 0
        for node in network:
            denom += binary_entropy(node.suratio)
        # perform injection
        for node in network:
            if player == "red":
                node.red += rbudget*(binary_entropy(node.suratio)/denom)
                node.blue += bbudget / network.num_nodes()
            if player == "blue":
                node.red = rbudget / network.num_nodes()
                node.blue = bbudget*(binary_entropy(node.suratio)/denom)
        # update superurn ratios
        network.update_superurn_ratios(player)
        # perform polya process at this timestep
        for node in network:
            # calculate draw probability
            if player == "red":
                prob_red = node.suratio
            if player == "blue":
                prob_red = 1 - node.suratio
            # perform draw
            if random.random() < prob_red:
                node.red += delta 
            else:
                node.blue += delta
        # calculate infection rate
        results[t] = network.update_superurn_ratios(player)
    return results

# binary entropy (by superurn?) population- and CI-weighted vs uniform
def besupopci_vinjection(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    delta = params['delta']
    # calculate initial ratios
    results = {}
    results[0] = network.update_superurn_ratios(player)
    # get total population
    total_pop = 0
    for node in network:
        total_pop += node.pop
    # begin polya process
    for t in range(1, timesteps+1):
        # get BE-CIR denominator for this timestep
        denom = 0
        for node in network:
            denom += binary_entropy(node.suratio)*node.degree*node.centrality*(1-node.ratio)*(node.red+node.blue)
        # perform injection at this timestep
        for node in network:
            if player == "red":
                node.red += (rbudget*binary_entropy(node.suratio)*node.degree*node.centrality*(1-node.ratio)*node.pop)/denom
                node.blue += bbudget / network.num_nodes()
            if player == "blue":
                node.red += rbudget / network.num_nodes()
                node.blue += (bbudget*binary_entropy(node.suratio)*node.degree*node.centrality*(1-node.ratio)*node.pop)/denom
        # update superurn ratios
        network.update_superurn_ratios(player)
        # perform polya process at this timestep
        for node in network: 
            # calculate draw probability
            if player == "red":
                prob_red = node.suratio
            if player == "blue":
                prob_red = 1 - node.suratio
            # perform draw
            if random.random() < prob_red:
                node.red += delta 
            else:
                node.blue += delta
        # calculate average urn ratio at this timestep
        results[t] = network.update_superurn_ratios(player)
    return results

