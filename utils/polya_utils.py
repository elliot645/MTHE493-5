from utils.graph_utils import *
import random

#--------------------------------------------------------------------------
# Classical Polya Process
#--------------------------------------------------------------------------

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
    results[0] = network.get_superurn_ratios(player)

    # begin polya process
    for t in range(1, timesteps+1):

        # perform draws across all nodes
        for node in network:

            # calculate delta values
            delta_red = rbudget / network.num_nodes()
            delta_blue = bbudget / network.num_nodes()
        
            # get superurn ratios
            if player == "red":
                prob_red = node.ratio
            if player == "blue":
                prob_red = 1 - node.ratio

            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue

        # calculate infection rate across network
        results[t] = network.get_superurn_ratios(player)

    return results

# int vs. uniform
def int_vdelta(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]

    # calculate initial infection rate
    results = {}
    results[0] = network.get_superurn_ratios(player)

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
            else:
                delta_red = rbudget / network.num_nodes()
                delta_blue = (bbudget*node.degree*node.centrality*(1-node.ratio)) / denom
            
            # get draw probability
            if player == "red":
                prob_red = node.ratio
            if player == "blue":
                prob_red = 1 - node.ratio

            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue

        # calculate infection rate
        results[t] = network.get_superurn_ratios(player)

    return results
            


