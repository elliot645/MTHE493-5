import pandas as pd
import random


"""
Function to read dataframe from csv file 
Input: filepath to voting data csv
Output: dataframe containing voting data from 2000 - 2020
"""
def read_voting_data(filepath):
    df = pd.read_csv(filepath)
    return df

"""
Function to create dict of initial and final conditions
Input: dataframe, start year, end year, state
Output: dict containing initial data
"""
def get_state_voting_data(voting_df, start_year, end_year, state):

    # Subset dataframe to state, years of interest
    start_df = voting_df[(voting_df["year"]  == start_year) & (voting_df["state_po"] == state)]
    end_df = voting_df[(voting_df["year"] == end_year) & (voting_df["state_po"] == state)]

    # Convert into list of dicts (each row is 1 dict)
    start_data = start_df.to_dict(orient="records")
    end_data = end_df.to_dict(orient="records")

    # Get list of unique counties
    counties = set(start_df["county_name"])

    # Create dict to hold results for entire model
    results = {
        county : {
            "start_votes" : {}, 
            "end_votes" : {}, 
            "model_votes" : {}
        } for county in counties
    }

    # Loop through dataset, add a dict of votes for each county
    for row in start_data:
        county = row["county_name"]
        party = row["party"]
        results[county]["start_votes"][party] = row["candidatevotes"]

    # Repeat for end year
    for row in end_data:
        county = row["county_name"]
        party = row["party"]
        results[county]["end_votes"][party] = row["candidatevotes"]

    return results 

"""
Function to calculate delta for each county
Input: results_dict
Output: none - results is modified
"""
def get_delta(results, timestep):

    # Calculate timestep
    n = timestep

    # Loop through every county, calculate expected delta
    for county in results:
        # Shorter notation
        R = results[county]["start_votes"]["REPUBLICAN"]
        T = R + results[county]["start_votes"]["DEMOCRAT"]
        end_R = results[county]["end_votes"]["REPUBLICAN"]
        end_T = end_R + results[county]["end_votes"]["DEMOCRAT"]
        Un = end_R / end_T

        # Calculation of delta
        exp_delta = R - (T*Un)
        sum = 0
        for y in list(range(1, n+1)):
            if y == n*Un:
                sum = sum 
            else:
                sum = sum + (1/(n*Un - y))*((R/T)**y)*(1-(R/T))**(n-y)
        exp_delta = exp_delta * sum

        # Add to results dict
        results[county]["delta"] = exp_delta
    return 


"""
Function to run polya process 
Input: results dict, timestep
Output: none - results is modified
"""
def polya_process(results, timestep):

    # Initialize model 
    for county in results["counties"]:
        results[county]["model_votes"]["red"] = results[county]["start_votes"]["REPUBLICAN"]
        results[county]["model_votes"]["blue"] = results[county]["start_votes"]["DEMOCRAT"]
    
    # Run model 
    n = timestep
    for t in range (1, n+1):
        # For every county in the country
        for county in results:
            # Faster notation
            r = results[county]["start_votes"]["REPUBLICAN"]
            b = results[county]["start_votes"]["DEMOCRAT"]
            prob_r = r/(r+b)
            delta = results[county]["delta"]

            # Perform draw and reinforcement
            if random.random() < prob_r:
                results[county]["model_votes"]["red"] += delta
            else:
                results[county]["model_votes"]["blue"] += delta
    
    return 
            
"""
Function to calculate error for each county
Input: results dict
Output: none - results is modified
"""
def get_error(results):

    # BOTH ERROR AND DELTA ARE CALCULATED IN TERMS OF R
    for county in results:
        start_R = results[county]["start_votes"]["REPUBLICAN"]
        start_B = results[county]["start_votes"]["DEMOCRAT"]
        start_U =  start_R / (start_R + start_B)
        model_R = results[county]["model_votes"]["red"]
        model_B = results[county]["model_votes"]["blue"]
        model_U = model_R / (model_R + model_B)

        error = (abs(model_U - start_U) / start_U)*100
        results[county]["error"] = error
    
    return 

"""
Function to print results to excel 
Input: results dict, fiepath to excel
Output: none - excel file is written
"""
def print_results(results, filepath, start_year, end_year, timestep, state):
    
    # Reformat results
    data = []
    for county in results:
        # Notation
        start_r = results[county]["start_votes"]["REPUBLICAN"]
        start_b = results[county]["start_votes"]["DEMOCRAT"]
        end_r = results[county]["end_votes"]["REPUBLICAN"]
        end_b = results[county]["end_votes"]["DEMOCRAT"]

        # Create row entry
        row = {
        "state" : state,
        "county" : county,
        "start_year" : start_year,
        "end_year" : end_year,
        "timesteps" : timestep,
        "start_R" : start_r,
        "start_B" : start_b,
        "end_R" : end_r,
        "end_B" : end_b,
        "start_U" : start_r / (start_r + start_b),
        "end_U" : end_r / (end_r+end_b),
        "delta" : results[county]["delta"],
        # "model_R" : results[county]["model_votes"]["red"],
        # "model_B" : results[county]["model_votes"]["blue"],
        # "error" : results[county]["error"]
        }
        data.append(row)
        
    # Convert results into a dataframe
    out_df = pd.DataFrame.from_records(data)

    # Write dataframe into excel sheet
    out_df.to_excel(filepath, index=False, startrow=0, startcol=0)

    return

    
