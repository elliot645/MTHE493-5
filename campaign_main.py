from utils.data_utils import *
from utils.graph_utils import *
from utils.polya_utils import *

"""
TO-DO:
- fill adjacency gaps in AK, HI, SD
    - debug centrality for AK, DC, HI, MD, MO, NV, VA
- convert voting data to JSON
- MAKE PASSIVE PLAYER USE POPULATION-WEIGHTED 
"""

#--------------------------------------------------------------
# Function to run numerous trials and track results: 
#--------------------------------------------------------------

def run_campaigns(trials, network, startvotes, params):
    # dict to track opinion over time for each strategy
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
                # reinforcement strategies 
                case 1:
                    results[strats[strat_id]][trial] = uniform_vdelta(network, params) 
                case 2:
                    results[strats[strat_id]][trial] = pop_vdelta(network, params)
                case 3:
                    results[strats[strat_id]][trial] = ci_vdelta(network, params)
                case 4:
                    results[strats[strat_id]][trial] = pop_ci_vdelta(network, params)
                # injection strategies
                case 5:
                    results[strats[strat_id]][trial] = uniform_vinjection(network, params)
                case 6:
                    results[strats[strat_id]][trial] = pop_vinjection(network, params)
                case 7:
                    results[strats[strat_id]][trial] = ci_vinjection(network, params)
                case 8:
                    results[strats[strat_id]][trial] = pop_ci_vinjection(network, params)
                case 9:
                    results[strats[strat_id]][trial] = besu_vinjection(network, params)
                case 10:
                    results[strats[strat_id]][trial] = besupopci_vinjection(network, params)
            print("Trial", trial, "complete.")
        print("Strategy", strat_id, "complete.")

    # get avg opinion at time t over all trials
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
    data_path = r'data\countypres_clean.xlsx'
    votes_sheet = 'countypres'
    fips_sheet = 'fipslist'
    adj_path = r'data\county_adjacency.csv'
    centrality_path = r'data\centrality_US.json'
    results_path = r'data\results.xlsx'

    #==============================================================
    # SET TRIAL PARAMETERS HERE
    #==============================================================

    state = 'CA'        # state=None --> whole country
                        # Don't use AK, DC, HI, MD, MO, NV, or VA - missing centrality 
    start_year = 2008   # Note: 2020 is missing data
    player = 'blue'     # 'blue' or 'red'
    rbudget = 100000
    bbudget = 100000
    delta = 100
    timesteps = 200
    trials = 20
    reinforcement_strats = {
        1 : 'Uniform',
        2 : 'Population-Weighted',                       
        3 : 'CIR-Weighted',
        4 : 'Pop-CIR-Weighted'
    }
    injection_strats = { 
        5 : 'Uniform',
        6 : 'Population-Weighted',
        7 : 'CIR-Weighted',
        8 : 'Pop-CIR-Weighted',
        9 : 'BE-Weighted'
        # 10 : "BE-CIR-Population-Weighted"   
    }
    finite_mem_injection = {
        5 : 'Uniform',
        6 : 'Population-Weighted',
        7 : 'CIR-Weighted',
        8 : 'Pop-CIR-Weighted'
    }

    #---------------------------------------------------------------
    
    # Get dict of viable nodes
    fipsdict = get_fipsdict(data_path, fips_sheet, state)

    # Get and set network topology
    neighbours = get_adjacency_dict(adj_path, fipsdict)       
    network = Graph()               
    network.set_topology(fipsdict, neighbours)       

    # Get and set node centrality                   
    centrality = get_centrality_dict(centrality_path)        
    network.set_centrality(centrality)      

    # Get initial conditions (set during experiment)          
    vdf = get_df(data_path, votes_sheet)                     
    startvotes = get_votes(vdf, fipsdict, start_year, state) 

    # Package trial parameters
    params = {                                               
        'player' : player,              # Active player
        'rbudget' : rbudget,            # Red's budget at each timestep
        'bbudget' : bbudget,            # Blue's budget at each timestep
        'timesteps' : timesteps,        # No. timesteps to run sim
        'strats' : injection_strats,    # Strategies to run
        'delta' : delta                 # For injection strategies
    }   

    #---------------------------------------------------------------

    # Run specified number of curing trials for given parameters
    results = run_campaigns(trials, network, startvotes, params)

    # Plot results
    for strat in results:
        xvals = []
        yvals = []
        for t in results[strat]:
            xvals.append(t)
            yvals.append(results[strat][t])
        plt.plot(xvals, yvals, label=strat)
    plt.legend()
    plt.title(state + ', ' + str(start_year) + ': ' + player + ', ' + 'budget=' + str(bbudget) + ', ' + 'delta=' + str(delta))
    plt.show()

    

        






