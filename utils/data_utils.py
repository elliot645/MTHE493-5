from utils.graph_utils import *
from utils.polya_utils import *
import pandas as pd
import time

#--------------------------------------------------------------------------
# Initialization Functions
#--------------------------------------------------------------------------

# Get dict like {state:{fips:county,...}}
def get_fipsdict(filepath, sheetname, state):
    start = time.time()

    # if no state specified, read for entire country
    if state is None:
        df = pd.read_excel(filepath, sheet_name=sheetname)
    # otherwise, only read FIPS for specified state
    else:
        df = pd.read_excel(filepath, sheet_name=sheetname)
        df = df[df["State"]==state]
    rows = df.to_dict(orient="records")
    fipsdict = {}
    for row in rows:
        fips = row["FIPS"]
        fipsdict[fips] = {}
        fipsdict[fips]["county"] = row["County"]
        fipsdict[fips]["state"] = row["State"]
        
    end = time.time()
    print("FIPS numbers retrieved:", round((end-start)*1000), "ms")
    return fipsdict

# Get dict like {fips:[neighbours],...}
def get_adjacency_dict(filepath, fipsdict):
    start = time.time()

    df = pd.read_csv(filepath)
    rows = df.to_dict(orient="records")
    adj_dict = {fips:set() for fips in fipsdict}
    viable = set(fipsdict.keys())
    for row in rows:
        county = row["county"]
        neighbour = row["neighbor"]
        if county in viable and neighbour in viable and county != neighbour:
            adj_dict[county].add(neighbour)  

    end = time.time()
    print("Adjacency retrieved:", round((end-start)*1000), "ms")
    return adj_dict

# Get voting data for specified year; return dict like {fips:{party:int, ...}}
def get_votes(filepath, sheetname, fipsdict, year, state):
    start = time.time()

    vdf = pd.read_excel(filepath, sheet_name=sheetname)
    if state is None:
        df = vdf[vdf["year"]==year]
    else:
        df = vdf[(vdf["year"]==year) & (vdf["state_po"]==state)]
    data = df.to_dict(orient="records")
    votes = {fips:{} for fips in fipsdict}
    for row in data:
        fips = row["county_fips"]
        party = row["party"]
        votes[fips][party] = row["candidatevotes"]

    end = time.time()
    print("Voting data for ", year, "retrieved:", round((end-start)*1000), "ms")
    return votes

#--------------------------------------------------------------------------
# Classic Polya Trial Functions
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# Campaign/Curing Trial Functions
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

# print results to excel
def print_curing_results(dict, filepath):
    out_df = pd.DataFrame.from_dict(dict)
    out_df.to_excel(filepath)
    print("Print complete.")
    return