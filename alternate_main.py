from alternate_model.voting_utils import *
from alternate_model.graph_utils import *
from alternate_model.polya_utils import *
from alternate_model.population_utils import *
from alternate_model.immigration_utils import *

import numpy as np


def run_experiment(start_year, end_year, timestep, voting_df, neighbours):

    # Get initial and final conditions
    start_votes = get_votes(voting_df, start_year)
    end_votes = get_votes(voting_df, end_year)

    # # Initialize graph
    graph = init_graph()

    # # Run Polya process
    polya(graph)

    # Get results
    model_votes = get_model_votes(graph)

    # Consolidate results
    results = consolidate(start_votes, end_votes, model_votes)

    # Get model error
    results = get_error(results)

    return results



if __name__ == "__main__":

    # Set filepaths 
    voting_path = "data\countypres.csv"
    adj_path = "data\countyadj.csv"
    death_path = "data\death_data.csv"
    population_path = "data\population.csv"
    results_path = "data\results.xlsx"

    # Read data
    voting_df = read_votes(voting_path)

    # Read and create county adjacency
    neighbours = create_county_adjacency_dict(adj_path)

    #---------------------------------------------------------------------------------

    print(voting_df["county_fips"])

    # Model parameters: 
    start_year = 2000
    end_year = 2004
    timestep = 48

    # Run experiment 
    results = run_experiment(start_year, end_year, timestep, voting_df, neighbours)

    # Print results
    # print_results(results_path, results, start_year, end_year, timestep)
