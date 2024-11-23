import pandas as pd

#--------------------------------------------------------------------------

# Read voting csv, do any tidying needed
# Input: filepath to voting data csv
# Output: dataframe containing voting data from 2000 - 2020
def read_votes(filepath):
    dtype = {"county_fips":"Int64"}
    df = pd.read_csv(filepath, dtype=dtype)
    return df

#--------------------------------------------------------------------------


# Get a dict of fips for each county
# Input: voting data
# Output: dict of form {state: {county:fips}}
def get_fips_dict(voting_df):

    fips_dict = {
        state : {} for state in pd.unique(voting_df["state_po"]) 
    }

    fips_df = voting_df[(voting_df["year"]==2000) & (voting_df["party"]=="DEMOCRAT")]
    fips_data = fips_df.to_dict(orient="records")
    for row in fips_data:
        state = row["state_po"]
        state_name = row["state"]
        county = row["county_name"]
        fips = row["county_fips"]
        fips_dict[state][county] = fips


    return fips_dict

#--------------------------------------------------------------------------


def create_county_adjacency_dict(file_path):
   
    adjacency_matrix = pd.read_csv(file_path, index_col=0)
    
    county_adjacency_dict = {}

    for county in adjacency_matrix.index:
        state = county.split()[-1] 
        if state not in county_adjacency_dict:
            county_adjacency_dict[state] = {}
        
        adjacent_counties = set(adjacency_matrix.loc[county][adjacency_matrix.loc[county] == 1].index.tolist())
        county_adjacency_dict[state][county] = adjacent_counties

    return county_adjacency_dict