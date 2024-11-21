from anna_functions import *
import random
import time


if __name__ == "__main__":

    # SET MODEL PARAMETERS HERE
    state = "FL"
    start_year = 2000
    end_year = 2004
    timestep = 48
    
    # read voting data
    readpath = voting_path = "data\countypres.csv"
    voting_df = read_voting_data(readpath)

    # set intitial conditions and final conditions
    results = get_state_voting_data(voting_df, start_year, end_year, state)

    # use initial and final conditions to calculate delta
    get_delta(results, timestep)

    # # run polya process
    # polya_process(results, timestep)

    # # calculate error for each county
    # get_error(results)

    # # print results to excel 
    outpath = r"C:\Users\annaw\Desktop\delta_results5.xlsx"
    print_results(results, outpath, start_year, end_year, timestep, state)




    

    