import pandas as pd



"""
Get voting numbers for given year
Input: dataframe and year of interest
Output: dict of {county:{name: , votes:{}}}
"""
def get_votes(voting_df, year):
    
    # Subset to year of interest
    df = voting_df[voting_df["year"] == year]

    # Convert to list of dicts (1 row per dict, keys are columns names)
    data = df.to_dict(orient="records")

    # Create dict to hold votes for each county
    counties = {}

    # Loop through dataset, adding dict of votes for each county
    for row in data:
        county_fips = row["county_fips"]
        county_name = row["county_name"]
        state = row["state_po"]
        party = row["party"]
        if county_fips not in counties.keys():
            counties[county_fips] = {}
        counties[county_fips]["county_name"] = county_name
        counties[county_fips]["state"] = state
        counties[county_fips][party] = row["candidatevotes"]
        
    return counties

#--------------------------------------------------------------------------

"""
Get dict of results for each county
Input: graph object
Output: dict of final votes from model
"""
def get_model_votes(graph):
    pass

#--------------------------------------------------------------------------

"""
Consolidate the three dicts into a printable dict
Input:
Output: dict of results formatted for printing
"""
def consolidate(start_votes, end_votes, model_votes):
    pass

#--------------------------------------------------------------------------

"""
Calculate error for each county
Input: consolidated results dict
Output: none - results is modified
"""
def get_error(results):
    for county in results:
        # Calculate actual and experimental proportion of red
        end_R = results[county]["end_votes"]["REPUBLICAN"]
        end_B = results[county]["end_votes"]["DEMOCRAT"]
        end_U =  end_R / (end_R + end_B)
        model_R = results[county]["model_votes"]["red"]
        model_B = results[county]["model_votes"]["blue"]
        model_U = model_R / (model_R + model_B)
        # Calculate error 
        error = error (abs(model_U - end_U) / end_U)*100
        results[county]["error"] = error
    return 

#--------------------------------------------------------------------------

"""
Print results to excel 
Input: results dict, fiepath to excel
Output: none - excel file is written
"""
def print_results(filepath, results, start_year, end_year, timestep):
    
    # Reformat results into a list of rows
    data = []
    for county in results:
        # Notation
        start_r = results[county]["start_votes"]["REPUBLICAN"]
        start_b = results[county]["start_votes"]["DEMOCRAT"]
        end_r = results[county]["end_votes"]["REPUBLICAN"]
        end_b = results[county]["end_votes"]["DEMOCRAT"]
        model_r = results[county]["model_votes"]["red"]
        model_b = results[county]["model_votes"]["blue"]
        start_U = start_r / (start_r + start_b)
        end_U = end_r / (end_r+end_b)
        model_U = model_r / (model_r + model_b)

        # Create row entry
        row = {
            "State" : county["state"],
            "County" : county["county_name"],
            "FIPS" : county,
            "Start Year" : start_year,
            "End Year" : end_year,
            "No. Timesteps" : timestep,
            "Initial R" : start_r,
            "Intial B" : start_b,
            "Final R" : end_r,
            "Final B" : end_b,
            "Model R" : model_r,
            "Model B" : model_b,
            "Initial U" : start_U,
            "Final U" : end_U,
            "Model U" : model_U
        }

        data.append(row)
    
    # Convert into dataframe
    out_df = pd.DataFrame.from_records(data)

    # Write dataframe into excel 
    out_df.to_excel(filepath, index=False, startrow=0, startcol=0)

    return