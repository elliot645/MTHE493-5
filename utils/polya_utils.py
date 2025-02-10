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

# population-weighted vs. uniform
def pop_vdelta(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]

    # calculate initial infection rate
    results = {}
    results[0] = network.get_superurn_ratios(player)

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
                prob_red = node.ratio
            if player == "blue":
                delta_red = rbudget / network.num_nodes()
                delta_blue = (node.pop/total_pop)*bbudget
                prob_red = 1 - node.ratio

            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue

        # calculate infection rate across network
        results[t] = network.get_superurn_ratios(player)

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
                prob_red = node.ratio
            if player == "blue":
                delta_red = rbudget / network.num_nodes()
                delta_blue = (bbudget*node.degree*node.centrality*(1-node.ratio)) / denom
                prob_red = 1 - node.ratio

            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue

        # calculate infection rate
        results[t] = network.get_superurn_ratios(player)

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
    results[0] = network.get_superurn_ratios(player)

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
                prob_red = node.ratio
            if player == "blue":
                delta_red = rbudget / network.num_nodes()
                delta_blue = ((node.pop*node.degree*node.centrality*(1-node.ratio))/denom)*bbudget
                prob_red = 1 - node.ratio

            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue

        # calculate infection rate
        results[t] = network.get_superurn_ratios(player)

    return results

#--------------------------------------------------------------------------
# Game Theory Experiment
#--------------------------------------------------------------------------

def run_curing_experiment(trials, network, startvotes, params):

    # dict to hold superurn ratios over time
    strats = params["strats"]
    results = {strats[strat_id]:{} for strat_id in strats}

    # run specified no. trials for each strategy
    for strat_id in strats:
        for trial in range(1, trials+1):

            # reset initial conditions
            for node in network:
                r = startvotes[node.id]["REPUBLICAN"]
                b = startvotes[node.id]["REPUBLICAN"]
                node.red = r
                node.blue = b
                node.pop = r + b
                
            # perform campaign
            match strat_id:
                case 1:
                    results[strats[strat_id]][trial] = uniform_vdelta(network, params) 
                case 2:
                    results[strats[strat_id]][trial] = pop_vdelta(network, params)
                case 3:
                    results[strats[strat_id]][trial] = ci_vdelta(network, params)
                case 4:
                    results[strats[strat_id]][trial] = pop_ci_vdelta(network, params)
            print("Trial", trial, "complete.")
        print("Strategy", strat_id, "complete.")

    # average the metric over all trials
    output = {strat:{} for strat in results}
    for strat in results:
        for t in range(0, params["timesteps"]+1):
            sum = 0
            count = 0
            for trial in results[strat]:
                sum += results[strat][trial][t]
                count += 1
            avg = sum / count
            output[strat][t] = avg

    return output