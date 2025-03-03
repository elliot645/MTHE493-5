from utils.data_utils import *
from utils.graph_utils import *
from utils.polya_utils import *

"""
TO-DO:
- fill adjacency gaps in AK, HI, SD
    - debug centrality for AK, DC, HI, MD, MO, NV, VA
- convert voting data to JSON
- plot results in main rather than write to excel
- MAKE PASSIVE PLAYER USE POPULATION-WEIGHTED 
"""

#--------------------------------------------------------------
# Function to run numerous trials and track results: 
#--------------------------------------------------------------

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
                b = startvotes[node.id]["DEMOCRAT"]
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
                case 5:
                     results[strats[strat_id]][trial] = ci_vinjection(network, params)
                case 6:
                    results[strats[strat_id]][trial] = pop_vinjection(network, params)
                case 7:
                    results[strats[strat_id]][trial] = besu_vinjection(network, params)
                case 8:
                    results[strats[strat_id]][trial] = besupopci_vinjection(network, params)


            print("Trial", trial, "complete.")
        print("Strategy", strat_id, "complete.")

    # average the superurn ratio over all trials
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

#--------------------------------------------------------------
# Main: 
#--------------------------------------------------------------

if __name__ == "__main__":

    # Set filepaths 
    data_path = r"data\countypres_clean.xlsx"
    votes_sheet = "countypres"
    fips_sheet = "fipslist"
    adj_path = r"data\county_adjacency.csv"
    centrality_path = r"data\centrality_US.json"
    results_path = r"data\results.xlsx"

    #===========================
    # SET TRIAL PARAMETERS HERE
    #===========================

    state = "NY"        # state=None --> whole country
    """Do not use AK, DC, HI, MD, MO, NV, or VA for now - missing centrality"""
    start_year = 2000   # Note: 2020 is missing data
    player = "blue" # "blue" or "red"
    rbudget = 100000
    bbudget = 100000
    timesteps = 200
    trials = 10
    strats = { 
        #1 : "Uniform Allocation via Delta",
        #2 : "Population-Weighted via Delta",                       
        #3 : "Centrality-Infection via Delta",
        #4 : "Population-Weighted Centrality Infection via Delta",
        5 : "Centrality-Infection via Injection vs. Uniform",
        6 : "Population-Weighted Injection vs. Uniform",
        7 : "Binary Entropy Injection vs. Uniform",
        8 : "Binary Entropy Centrality Population Injection vs. Uniform"
    }

    #---------------------------------------------------------------
    
    # The following parameters are fixed for all trials:
    fipsdict = get_fipsdict(data_path, fips_sheet, state)    # Nodes
    neighbours = get_adjacency_dict(adj_path, fipsdict)      # Edges
    network = Graph()                                        #
    network.set_topology(fipsdict, neighbours)               # Graph topology           
    centrality = get_centrality_dict(centrality_path)        # 
    network.set_centrality(centrality)                       # Node centrality 
    vdf = get_df(data_path, votes_sheet)                     #
    startvotes = get_votes(vdf, fipsdict, start_year, state) # Initial conditions  
    params = {                                               # Game parameters:
        "player" : player,                                   # Active player
        "rbudget" : rbudget,                                 # Red's budget at each t
        "bbudget" : bbudget,                                 # Blue's budget at each t
        "timesteps" : timesteps,                             # No. timesteps to run sim
        "strats" : strats,                                   # Strategies to run
        "delta" : 50                                         # For injection strategies
    }   

    #---------------------------------------------------------------

    # Run specified number of curing trials for given parameters
    output = run_curing_experiment(trials, network, startvotes, params)
    print_curing_results(output, results_path)

        






