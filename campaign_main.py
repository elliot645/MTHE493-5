from utils.graph_utils import *
from utils.polya_utils import *
from utils.approx_utils import *
import json
import pandas as pd
import networkx as nx
import numpy as np


# run all strategies one one state for given year
def run_campaign(network, params, trials, votesdict):

    # dict to track opinion over time for each strategy
    strats = params["strats"]
    results = {strats[strat_id]:{} for strat_id in strats}

    # run specified no. trials for each strategy
    for strat_id in strats:
        for trial in range(1, trials+1):

            # reset initial conditions
            for node in network:
                node.red = votesdict[startyear][node.id]['REPUBLICAN']
                node.blue = votesdict[startyear][node.id]['DEMOCRAT']
                node.pop = node.red + node.blue
                
            # perform campaign
            match strat_id:
                # reinforcement strategies 
                case 1:
                    results[strats[strat_id]][trial] = uniform_vdelta(network, params) 
                case 2:
                    results[strats[strat_id]][trial] = pop_vdelta(network, params)
                case 3: 
                    results[strats[strat_id]][trial] = be_vdelta(network, params)
                case 4:
                    results[strats[strat_id]][trial] = ci_vdelta(network, params)
                case 5:
                    results[strats[strat_id]][trial] = pop_ci_vdelta(network, params)
                case 6:
                    results[strats[strat_id]][trial] = be_pop_ci_vdelta(network, params)

                # injection strategies
                case 6:
                    results[strats[strat_id]][trial] = uniform_vinjection(network, params)
                case 7:
                    results[strats[strat_id]][trial] = pop_vinjection(network, params)
                case 8:
                    results[strats[strat_id]][trial] = be_vinjection(network, params)
                case 9:
                    results[strats[strat_id]][trial] = ci_vinjection(network, params)
                case 10:
                    results[strats[strat_id]][trial] = pop_ci_vinjection(network, params)
                case 11:
                    results[strats[strat_id]][trial] = be_pop_ci_vinjection(network, params)

                # memory injection strategies
                

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

#==================================================================

if __name__ == "__main__":

    # Set filepaths 
    fips_path = r'data\statefips.json'    # ignore AK, HI
    adj_path = r'data\countyadj.json'
    centrality_path = r'data\centrality.json'
    votes_path = r'data\votingdata.json'
    po_path = r'data\state_PO.json'

    # set up dicts
    fipsdict = get_dict_from_json(fips_path)
    adjdict = get_dict_from_json(adj_path)
    centralitydict = get_dict_from_json(centrality_path)
    votesdict = get_dict_from_json(votes_path)
    podict = get_dict_from_json(po_path)

    # create dict of graphs (one per state)
    graphs = {}
    for state in fipsdict:
        network = Graph()
        network.set_state_topology(state, fipsdict, adjdict)
        network.set_state_centrality(state, centralitydict)
        graphs[state] = network

    #======================================
    # SET EXPERIMENT PARAMETERS HERE
    #======================================

    # define parameters
    draws = 100
    trials = 50
    rbudget = 10000
    bbudget = 10000
    delta = 100

    # set strategies
    reinforcement_strats = {
        1 : 'Uniform',
        2 : 'Population-Weighted',   
        3 : 'BE-Weighted',                    
        4 : 'CIR-Weighted',
        5 : 'Pop-CIR-Weighted',
        6 : 'BE-Pop-CIR Weighted'
    }
    injection_strats = { 
        6 : 'Uniform',
        7 : 'Population-Weighted',
        8 : 'BE-Weighted',
        9 : 'CIR-Weighted',
        10 : 'Pop-CIR-Weighted',
        11 : 'BE-Pop-CIR-Weighted'   
    }
    injection_w_memory = {
        12 : 'Uniform',
        13 : 'Population-Weighted',
        14 : 'CIR-Weighted',
        15 : 'Pop-CIR-Weighted'
    } 

    #======================================
    # GET RESULTS HERE
    #======================================

    # set filepath and strategies to use
    results_path = 'data/Campaign Results/Injection/PDF/'   # SET OUTPUT PATH HERE
    params = {   
        'strats' : injection_strats,                        # SET STRATEGY TYPE HERE  
        'timesteps' : draws,                                                          
        'rbudget' : rbudget,           
        'bbudget' : bbudget,            
        'delta' : delta     
    }  

    for player in ['red', 'blue']:
        params['player'] = player

        for startyear in ['2000', '2004', '2008', '2012', '2016']:
            params['startyear'] = startyear

            for state in graphs:
                network = graphs[state]

                # run multiple trials of each strategy
                results = run_campaign(network, params, trials, votesdict)
                
                # plot each strategy on same figure
                for strat in results:
                    xvals = []
                    yvals = []
                    for t in results[strat]:
                        xvals.append(t)
                        yvals.append(results[strat][t])
                    plt.plot(xvals, yvals, label=strat)

                # label and title figure, then save
                plt.legend()
                plt.title(state + ', ' + startyear + ': ' + player.capitalize() + ' Player')
                # plt.savefig(results_path + state + '_' + player.capitalize() + '_' + startyear)          # save as PNG
                plt.savefig(results_path + state + '_' + player.capitalize() + '_' + startyear + '.pdf') # save as PDF

                # clear figure for next state
                plt.clf()

                print(state, 'complete.')
            print(startyear, 'complete.')
        print(player, 'complete.')










