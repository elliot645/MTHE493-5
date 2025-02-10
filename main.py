from utils.data_utils import *
from utils.graph_utils import *
from utils.polya_utils import *

"""
TO-DO:
-set adjacency for Hawaii, Arkansas, Oglala Lakota SD; currently have no neighbours
-rather than pick the active player, set a strategy for each player?
-choose which metric to minimize in a two-player game
"""
#-------------------------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    # Set filepaths 
    data_path = r"data\countypres_clean.xlsx"
    votes_sheet = "countypres"
    fips_sheet = "fipslist"
    adj_path = r"data\county_adjacency.csv"
    results_path = r"data\results.xlsx"

    #================================================
    # SET TRIAL PARAMETERS HERE:
    state = "PA"                    # state=None --> whole country
    start_year = 2000               # Note: 2020 is missing data
    player = "blue"
    rbudget = 10000
    bbudget = 10000
    timesteps = 200
    trials = 100
    strats = { 
        1 : "Uniform Allocation via Delta",
        2 : "Population-Weighted via Delta",                       
        3 : "Centrality-Infection via Delta",
        4 : "Population-Weighted Centrality Infection via Delta"  
    }
    #================================================

    # The following parameters are fixed for all trials:
    fipsdict = get_fipsdict(data_path, fips_sheet, state)    # Nodes
    neighbours = get_adjacency_dict(adj_path, fipsdict)      # Edges
    network = Graph()                                        # Graph 
    network.set_topology(fipsdict, neighbours)               # Graph topology           
    network.get_centrality()                                 # Node centrality  
    startvotes = get_votes(data_path, votes_sheet,           # Initial conditions:
        fipsdict, start_year, state)     
    params = {                                               # Game parameters:
        "player" : player,                                   # Active player
        "rbudget" : rbudget,                                 # Red's budget at each t
        "bbudget" : bbudget,                                 # Blue's budget at each t
        "timesteps" : timesteps,                             # No. timesteps to run sim
        "strats" : strats                                    # Strategies to run
    }   

    # Run specified number of curing trials for given parameters
    output = run_curing_experiment(trials, network, startvotes, params)
    print_curing_results(output, results_path)

