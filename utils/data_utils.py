from utils.graph_utils import *
from utils.polya_utils import *
import pandas as pd
import time
import json

#--------------------------------------------------------------------------
# Initialization 
#--------------------------------------------------------------------------

# Get dict like {fips:{county:county,state:state}}
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

def get_centrality_dict(filepath):
    with open(filepath) as json_file:
        return json.load(json_file)

def get_df(filepath, sheetname):
    start = time.time()
    vdf = pd.read_excel(filepath, sheet_name=sheetname)
    end = time.time()
    print("Excel sheet read:", round((end-start)*1000), "ms")
    return vdf

# Get voting data for specified year; return dict like {fips:{party:int, ...}}
def get_votes(vdf, fipsdict, year, state):
    start = time.time()
    if state is None:
        df = vdf[vdf["year"]==year]
    else:
        df = vdf[(vdf["year"]==year) & (vdf["state_po"]==state)]
    rows = df.to_dict(orient="records")
    votes = {fips:{} for fips in fipsdict}
    for row in rows:
        fips = row["county_fips"]
        party = row["party"]
        votes[fips][party] = row["candidatevotes"]

    end = time.time()
    print("Voting data for ", year, "retrieved:", round((end-start)*1000), "ms")
    return votes

#--------------------------------------------------------------------------
# Classic Polya Trials
#--------------------------------------------------------------------------

# add initial and final conditions to each node

# calculate error


#--------------------------------------------------------------------------
# Campaign/Curing Trials
#--------------------------------------------------------------------------

# print results to excel
def print_curing_results(dict, filepath):
    out_df = pd.DataFrame.from_dict(dict)
    out_df.to_excel(filepath)
    print("Print complete.")
    return