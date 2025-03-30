from utils.graph_utils import *
from utils.polya_utils import *
from utils.approx_utils import *
import json
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.stats import beta

if __name__ == "__main__":

    # filepaths
    fips_path = r'data\statefips.json'    # ignore AK, HI
    adj_path = r'data\countyadj.json'
    votes_path = r'data\votingdata.json'
    po_path = r'data\state_PO.json'
    results_path = r'data\results.xlsx'

    # set up dicts
    fipsdict = get_dict_from_json(fips_path)
    adjdict = get_dict_from_json(adj_path)
    votesdict = get_dict_from_json(votes_path)
    podict = get_dict_from_json(po_path)

    # create dict of graphs (one per state) and set topology
    graphs = {}
    for state in fipsdict:
        network = Graph()
        network.set_state_topology(state, fipsdict, adjdict)
        graphs[state] = network
        
    # set experiment parameters
    startyear = '2000'
    timesteps = 200
    trials = 100

    dataframes = {}
    for endyear in ['2004', '2008', '2012', '2016']:
        results = {}
        for state in graphs:
            network = graphs[state]
            # get data that won't be altered in trials
            for node in network:
                endr = votesdict[endyear][node.id]['REPUBLICAN']
                endb = votesdict[endyear][node.id]['DEMOCRAT']
                node.real_ratio = endr/(endr+endb)
                node.delta = 1
            # get average error across all trials
            total_error = 0
            for trial in range(0,trials):
                # reset initial conditions
                for node in network:
                    node.red = votesdict[startyear][node.id]['REPUBLICAN']
                    node.blue = votesdict[startyear][node.id]['DEMOCRAT']
                    node.pop = node.red + node.blue
                # perform polya process
                trial_error, total_pop = network_polya(network, timesteps)
                total_error += trial_error
            # add to results
            avg_error = total_error/trials
            results[podict[state]] = {
                'Avg Error' : round(avg_error*100,2),
                'Total Votes' : total_pop
            }
            print(state, 'complete.')
        # create dataframe from results for this year
        dataframes[endyear] = pd.DataFrame.from_dict(results, orient='index')
        print(endyear, 'complete.')

    # write to excel sheet
    with pd.ExcelWriter(results_path) as writer:
        for endyear in dataframes:
            dataframes[endyear].to_excel(writer, sheet_name=startyear+'-'+endyear)

    

    



    

            
    
   






    
    









    

    





    

            
