from utils.data_utils import *
from utils.graph_utils import *
from utils.polya_utils import *

"""
TO-DO:
------
- fill adjacency gaps in AK, HI, SD
- debug centrality for AK, DC, HI, MD, MO, NV, VA
- plot results in main rather than write to excel
"""


if __name__ == "__main__":

    # Set filepaths 
    data_path = r"data\countypres_clean.xlsx"
    votes_sheet = "countypres"
    fips_sheet = "fipslist"
    adj_path = r"data\county_adjacency.csv"
    centrality_path = r"data\centrality_US.json"
    results_path = r"data\results.xlsx"

    #================================================
    # SET TRIAL PARAMETERS HERE:
    state = "NY"        # state=None --> whole country
    """Do not use AK, DC, HI, MD, MO, NV, or VA for now - missing centrality"""
    start_year = 2000   # Note: 2020 is missing data
    player = "blue"
    rbudget = 10000
    bbudget = 10000
    timesteps = 200
    trials = 100
    reinforcement_strats = { 
        1 : "Uniform Allocation via Delta",
        2 : "Population-Weighted via Delta",                       
        3 : "Centrality-Infection via Delta",
        4 : "Population-Weighted Centrality Infection via Delta"  
    }
    injection_strats = {}
    #================================================

    # The following parameters are fixed for all trials:
    fipsdict = get_fipsdict(data_path, fips_sheet, state)    # Nodes
    neighbours = get_adjacency_dict(adj_path, fipsdict)      # Edges
    network = Graph()                                        #
    network.set_topology(fipsdict, neighbours)               # Graph topology           
    centrality = get_centrality_dict(centrality_path)        # 
    network.set_centrality(centrality)                       # Node centrality   
    startvotes = get_votes(data_path, votes_sheet,           # Initial conditions
        fipsdict, start_year, state)     
    params = {                                               # Game parameters:
        "player" : player,                                   # Active player
        "rbudget" : rbudget,                                 # Red's budget at each t
        "bbudget" : bbudget,                                 # Blue's budget at each t
        "timesteps" : timesteps,                             # No. timesteps to run sim
        "strats" : reinforcement_strats                      # Strategies to run
    }   

    # Run specified number of curing trials for given parameters
    output = run_curing_experiment(trials, network, startvotes, params)
    print_curing_results(output, results_path)






