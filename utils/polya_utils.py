from utils.graph_utils import *
import random

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
# Curing/Game Theory Campaign
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

"""
- uniform injection
- population-weighted
- centrality-infection weighted
- population and centrality-infection weighted


- Anna: delta_i for each node (delta = K*h_b(U_0))
    - delta_i will be an attribute of each node 
"""