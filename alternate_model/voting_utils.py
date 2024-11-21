import pandas as pd


"""
Read dataframe from csv file 
Input: filepath to voting data csv
Output: dataframe containing voting data from 2000 - 2020
"""
def read_votes(filepath):
    df = pd.read_csv(filepath)
    return df


"""
Create dict of initial and final conditions
Input: dataframe, start year, end year, state
Output: dict containing initial data
"""
def get_votes(voting_df, year):
    pass



"""
Get dict of results for each county
Input: graph object
Output: dict of final votes from model
"""
def get_model_votes(graph):
    pass


"""
Consolidate the three dicts into a printable dict
Input:
Output: dict of results formatted for printing
"""
def consolidate(start_votes, end_votes, model_votes):
    pass


"""
Calculate error for each county
Input: results dict
Output: none - results is modified
"""
def get_error(start_votes, end_votes, model_votes):
    pass



"""
Print results to excel 
Input: results dict, fiepath to excel
Output: none - excel file is written
"""
def print_results(results, filepath):
    pass