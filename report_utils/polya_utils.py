import random, math

#==========================================================================

def binary_entropy(p):
    if 0 < p and p < 1:
        return p*math.log2(p) + (1-p)*math.log2(1-p)
    else:
        return 0

#==========================================================================
# Classical Polya Process
#==========================================================================

# classical polya process (infinite memory)
# returns population-weighted relative error for state
def classical_polya(network, timesteps):
    # set initial ratios
    for node in network:
        node.ratio = node.red/(node.red+node.blue)
    # begin process
    for t in range(0, timesteps):
        for node in network:
            # perform draw
            if random.random() < node.ratio:
                node.red += node.delta
            else:
                node.blue += node.delta
            # update ratio
            node.ratio = node.red/(node.red+node.blue)
    # calculate average relative error across state
    sum = 0
    total = 0
    for node in network:
        sum += (abs(node.ratio-node.real_ratio)/node.real_ratio)*node.pop
        total += node.pop
    error = sum/total
    return error, total

# network polya process, infinite memory
# returns population-weighted relative error             
def network_polya(network, timesteps):
    # perform network process
    network.update_superurn_ratios('red')
    for t in range (1, timesteps+1):
        for node in network:
            if random.random() < node.suratio:
                node.red += node.delta
            else:
                node.blue += node.delta
        network.update_superurn_ratios('red')
    # get error
    sum = 0
    total = 0
    for node in network:
        sum += (abs(node.ratio-node.real_ratio)/node.real_ratio)*node.pop
        total += node.pop
    error = sum/total
    return error, total


def classical_polya_memory():
    pass

def network_polya_memory():
    pass


#==========================================================================
# Curing via Reinforcement
#==========================================================================

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

def be_vdelta(network, params):
    # unbox params
    player = params["player"]
    rbudget = params["rbudget"]
    bbudget = params["bbudget"]
    timesteps = params["timesteps"]
    # calculate initial infection rate
    results = {}
    results[0] = network.update_superurn_ratios(player)
    for t in range(1, timesteps+1):
        # get BE denominator at this timestep 
        denom = 0
        for node in network:
            denom += binary_entropy(node.suratio)
        # calculate delta values
        for node in network:
            if player == "red":
                delta_red = rbudget*(binary_entropy(node.ratio)/denom)
                delta_blue = bbudget / network.num_nodes()
                prob_red = node.suratio
            if player == "blue":
                delta_red = rbudget / network.num_nodes()
                delta_blue = bbudget*(binary_entropy(node.ratio)/denom)
                prob_red = 1 - node.suratio
        # perform draw
        for node in network:
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue
        # calculate infection rate
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

# population- and centrality-infection-weighted vs. uniform
def be_pop_ci_vdelta(network, params):
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
    for t in range(1, timesteps+1):
        # get CIR denominator for this timestep
        denom = 0
        for node in network:
            denom += binary_entropy(node.ratio)*node.degree*node.centrality*(1-node.ratio)*(node.red+node.blue)
        
        for node in network:
            # calculate delta values
            if player == "red":
                delta_red = (rbudget*binary_entropy(node.ratio)*node.degree*node.centrality*(1-node.ratio)*node.pop)/denom
                delta_blue = bbudget / network.num_nodes()
                prob_red = node.suratio
            if player == "blue":
                delta_red = rbudget / network.num_nodes()
                delta_blue =  (bbudget*binary_entropy(node.ratio)*node.degree*node.centrality*(1-node.ratio)*node.pop)/denom                
                prob_red = 1 - node.suratio
            # perform draw
            if random.random() < prob_red:
                node.red += delta_red
            else:
                node.blue += delta_blue
        # calculate infection rate
        results[t] = network.update_superurn_ratios(player)
    return results


#==========================================================================
# Curing via Injection
#==========================================================================

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

# Population-weighted vs. uniform
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

# Binary entropy (of superurn) vs. uniform 
def be_vinjection(network, params):
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
            denom += binary_entropy(node.ratio)
        # perform injection
        for node in network:
            if player == "red":
                node.red += rbudget*(binary_entropy(node.ratio)/denom)
                node.blue += bbudget / network.num_nodes()
            if player == "blue":
                node.red += rbudget / network.num_nodes()
                node.blue += bbudget*(binary_entropy(node.ratio)/denom)
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

# Population- and CIR-weighted vs. uniform
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
        

# Binary entropy (of superurn)-, population-, and CI-weighted vs uniform
def be_pop_ci_vinjection(network, params):
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
            denom += binary_entropy(node.ratio)*node.degree*node.centrality*(1-node.ratio)*(node.red+node.blue)
        # perform injection at this timestep
        for node in network:
            if player == "red":
                node.red += (rbudget*binary_entropy(node.ratio)*node.degree*node.centrality*(1-node.ratio)*node.pop)/denom
                node.blue += bbudget / network.num_nodes()
            if player == "blue":
                node.red += rbudget / network.num_nodes()
                node.blue += (bbudget*binary_entropy(node.ratio)*node.degree*node.centrality*(1-node.ratio)*node.pop)/denom
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
