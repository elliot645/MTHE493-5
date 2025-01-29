from alternate_utils.data_utils import *
from alternate_utils.graph_utils import *
from alternate_utils.polya_utils import *

import numpy as np

def run_experiment(fips_dict, start_votes, end_votes, timestep, neighbours=None):

    # Initialize graph
    graph = init_graph(start_votes, neighbours, fips_dict)

    # Check that nodes match keys
    nkeys = len(fips_dict)
    nnodes = len(graph.nodes)
    if nnodes != nkeys:
        print("Number of nodes does not match number of keys! Ending experiment.")
        return
        
    # Run Polya process
    polya_i_i_c(graph, 1, timestep)

    # Get results
    results = get_results(graph, start_votes, end_votes, fips_dict)

    return results 


if __name__ == "__main__":

    # Set filepaths 
    fips_path = r"data\fips.xlsx"
    voting_path = r"data\countypres.csv"
    adj_path = r"data\countyadj.csv"
    death_path = r"data\death_data.csv"
    population_path = r"data\population.csv"
    results_path = r"data\results.xlsx"
    error_path = r"data\error_results.xlsx"

    # Get FIPS numbers
    fips_dict = get_fips_dict(fips_path)

    # Read voting data
    voting_df = read_votes(voting_path)
 
    #----------------------------------------------------------------

    # # Model parameters: 
    # start_year = 2000
    # end_year = 2016

    # # Retrieve initial conditions
    # start_votes, end_votes = retrieve_data(voting_df, fips_dict, start_year, end_year)
    
    # # Determine graph edges
    # neighbours = None

    # # Determine average error for each timestep
    # error_dict = {}
    # for timestep in [1, 10, 100, 1000]:
    #     for i in range(0,100):
    #         total_error = 0
    #         results = run_experiment(fips_dict, start_votes, end_votes, timestep, neighbours)
    #         sum = 0
    #         sum_count = 0
    #         for fips in results:
    #             if results[fips]["error"] != "NA":
    #                 sum += results[fips]["error"]
    #                 sum_count += 1
    #         total_error += sum / sum_count
    #     avg_error = total_error / 50
    #     error_dict[timestep] = avg_error
    #     print("Timesteps = " + str(timestep) + " complete.")
    # print_dict(error_dict, error_path)

    error_dict = {}
    start_year = 2000
    start_votes = get_votes(voting_df, fips_dict, start_year)
    end_year = 2004
    while end_year < 2020:
        end_votes = get_votes(voting_df, fips_dict, end_year)
        sum = 0
        for i in range(0,100):
            results = run_experiment(fips_dict, start_votes, end_votes, 100)
            sum += get_error(results)
        avg_error = sum / i
        error_dict[end_year] = avg_error*100
        end_year += 4
    print_dict(error_dict, error_path)


"""
analysis = {
    fips : {
        state : state_po
        total_votes  :
        total_2000 : 
        U_2000
    }
}
"""




    


