from utils.graph_utils import *
from utils.polya_utils import *
from utils.approx_utils import *
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":

    # filepaths
    fips_path = 'data/statefips.json'    # ignore AK, HI
    adj_path = 'data/countyadj.json'
    votes_path = 'data/votingdata.json'
    po_path = 'data/state_PO.json'
    out_path = 'data/mapresults.xlsx'

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
    endyear = '2004'
    draws = 200
    trials = 100
    delta_bar = 5000000

    total_pop = 0
    # set initial conditions
    for state in graphs:
        network = graphs[state]
        for node in network: 
            node.red = votesdict[startyear][node.id]['REPUBLICAN']
            node.blue = votesdict[startyear][node.id]['DEMOCRAT']
            node.pop = node.red + node.blue
            total_pop += node.pop
            endr = votesdict[endyear][node.id]['REPUBLICAN']
            endb = votesdict[endyear][node.id]['DEMOCRAT']
            node.real_ratio = endr/(endr+endb)

    results = {}
    # run simulation 
    for state in graphs:
        network = graphs[state]
        total_classical_error = 0
        total_network_error = 0

        for trial in range(0,trials):
            # set initial conditions
            for node in network:
                node.red = votesdict[startyear][node.id]['REPUBLICAN']
                node.blue = votesdict[startyear][node.id]['DEMOCRAT']
                node.pop = node.red + node.blue
                node.delta = (node.pop/total_pop)*delta_bar
            # run process
            classical_error, state_pop = classical_polya(network, draws)
            total_classical_error += classical_error
            network_error, state_pop = network_polya(network, draws)
            total_network_error += network_error

        # add to results
        avg_classical_error = total_classical_error/trials
        avg_network_error = total_network_error/trials
        results[podict[state]] = {
                'Avg Classic Error' : round(avg_classical_error*100, 2),
                'Avg Network Error' : round(avg_network_error*100, 2),
                'State Population' : state_pop
            }
        print(state, 'complete.')

    df = pd.DataFrame.from_dict(results, orient='index')
    df.to_excel(out_path)

    
    


    

    



    

            
    
   






    
    









    

    





    

            
