from voting_utils import *
from graph_utils import *
from polya_utils import *
from population_utils import *
from immigration_utils import *



def run_experiment(start_year, end_year, timestep, voting_df, neighbours):

    # Get initial and final conditions
    start_votes = get_votes(voting_df, start_year)
    end_votes = get_votes(voting_df, end_year)

    # Initialize graph
    graph = init_graph()

    # Run Polya process
    polya(graph)

    # Get results
    model_votes = get_model_votes(graph)

    # Consolidate results
    results = consolidate(start_votes, end_votes, model_votes)

    # Get model error
    results = get_error(results)

    return results



if __name__ == "__main__":

    # SET MODEL PARAMETERS HERE
    start_year = 2000
    end_year = 2004
    timestep = 48
    
    # Set filepaths 
    voting_path = ""
    adj_path = ""
    death_path = ""
    population_path = ""
    results_path = ""

    # Read data
    voting_df = read_votes(voting_path)

    # Read and create county adjacency
    neighbours = create_county_adjacency_dict("data\countyadj.csv")

    # Run experiment 
    results = run_experiment(start_year, end_year, timestep, voting_df, neighbours)

    # Print results
    print_results(results, results_path)
