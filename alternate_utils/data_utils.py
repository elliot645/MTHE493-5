import pandas as pd

"""
Get a dict of fips for each county
Input: voting data
Output: dict of form {fips: {county_name:string, state:string}}
"""
def get_fips_dict(filepath):

    fips_dict = {}

    fips_df = pd.read_excel(filepath, sheet_name="fips")
    rows = fips_df.to_dict(orient="records")

    for row in rows:
        fips = row["fips"]
        county_name = row["county"]
        state = row["state po"]
        if fips not in fips_dict.keys():
            fips_dict[fips] = {}
        fips_dict[fips]["county_name"] = county_name
        fips_dict[fips]["state"] = state
        
    return fips_dict

#--------------------------------------------------------------------------

"""
Read voting csv, do any tidying needed
Input: filepath to voting data csv
Output: dataframe containing voting data from 2000 - 2020
"""
def read_votes(filepath):
    dtype = {"county_fips":"Int64"}
    df = pd.read_csv(filepath, dtype=dtype)
    return df

#--------------------------------------------------------------------------

"""
Get voting numbers for given year
Input: dataframe and year of interest
Output: dict like {county_fips:{party:int, ... , party:int}}
"""
def get_votes(voting_df, fips_dict, year):
    
    # Subset to year of interest
    df = voting_df[voting_df["year"] == year]

    # Convert to list of dicts (1 row per dict, keys are columns names)
    data = df.to_dict(orient="records")

    # Create dict to hold votes for each county
    votes_by_county = {}
    fips_test = set(fips_dict)

    # Loop through dataset, adding dict of votes for each county
    for row in data:
        county_fips = row["county_fips"]
        if county_fips is not None:
            party = row["party"]
            if county_fips not in votes_by_county.keys():
                votes_by_county[county_fips] = {}
            votes_by_county[county_fips][party] = row["candidatevotes"]
            if county_fips in fips_test:
                fips_test.remove(county_fips)
        
    print("For year = " + str(year) + ":")
    # for counties missing from the dataset, set votes to NA
    if len(fips_test) != 0:
        print("    Missing data:   " + str(len(fips_test)) + " rows - filled with NA.")
        for fips in fips_test:
            votes_by_county[fips] = {}
            votes_by_county[fips]["REPUBLICAN"] = "NA"
            votes_by_county[fips]["DEMOCRAT"] = "NA"

    # if both values are 0, set to "NA"
    count = 0
    for fips in votes_by_county:
        if votes_by_county[fips]["DEMOCRAT"] == 0 and votes_by_county[fips]["REPUBLICAN"] == 0:
            votes_by_county[fips]["REPUBLICAN"] = "NA"
            votes_by_county[fips]["DEMOCRAT"] = "NA"
            count += 1
    print("    All-zero data: " + str(count) + " rows - replaced with NA.")

    return votes_by_county

#--------------------------------------------------------------------------

"""
Get dict of results for each county
Input: graph object
Output: dict of start votes, end votes, modelled votes, ratios, and error
"""
def get_results(graph, start_votes, end_votes, fips_dict):
    
    results = {}
    for node_id, node in graph.nodes.items():
        fips = node.id
        results[fips] = {}

        start_r = start_votes[fips]["REPUBLICAN"]
        start_b = start_votes[fips]["DEMOCRAT"]
        end_r = end_votes[fips]["REPUBLICAN"]
        end_b = end_votes[fips]["DEMOCRAT"]
        model_r = node.red
        model_b = node.blue
        if start_r != "NA" and start_b != "NA":
            start_U = start_r/(start_r+start_b)
        else:
            start_U = "NA"
        if end_r != "NA" and end_b != "NA":
            end_U = end_r/(end_r+end_b)
        else:
            end_U = "NA"
        if model_r != "NA" and model_b != "NA":
            model_U = model_r/(model_r+model_b)  
        else:
            model_U = "NA"

        results[fips]["county_name"] = fips_dict[fips]["county_name"]
        results[fips]["state"] = fips_dict[fips]["state"]
        results[fips]["start_red"] = start_r
        results[fips]["start_blue"] = start_b
        results[fips]["end_red"] = end_r
        results[fips]["end_blue"] = end_b
        results[fips]["model_red"] = model_r
        results[fips]["model_blue"] = model_b
        results[fips]["start_U"] = start_U
        results[fips]["end_U"] = end_U
        results[fips]["model_U"] = model_U
        if model_U != "NA" and end_U != "NA":
            results[fips]["error"] = (abs(model_U-end_U) / end_U)
        else:
            results[fips]["error"] = "NA" 

    return results

#--------------------------------------------------------------------------

def get_error(results):

    sum = 0
    count = 0
    for fips in results:
        if results[fips]["error"] != "NA":
            sum += results[fips]["error"]
            count += 1
    error = sum / count

    return error
    

#--------------------------------------------------------------------------

"""
Print results to excel 
Input: results dict, filepath to excel
Output: none - excel file is written
"""
def print_results(results, start_year, end_year, timestep, fips_dict, filepath):
    
    # Reformat results into a list of rows
    data = []
    for fips in results:
        # Create row entry
        row = {
            "State" : fips_dict[fips]["state"],
            "County" : fips_dict[fips]["county_name"],
            "FIPS" : fips,
            "Start Year" : start_year,
            "End Year" : end_year,
            "Timesteps" : timestep,
            "Initial R" : results[fips]["start_red"],
            "Intial B" : results[fips]["start_blue"],
            "Final R" : results[fips]["end_red"],
            "Final B" : results[fips]["end_blue"],
            "Model R" : results[fips]["model_red"],
            "Model B" : results[fips]["model_blue"],
            "Initial U" : results[fips]["start_U"],
            "Final U" : results[fips]["end_U"],
            "Model U" : results[fips]["model_U"],
            "% Error" : results[fips]["error"]
        }
        data.append(row)
    
    # Convert into dataframe
    out_df = pd.DataFrame.from_records(data)

    # Write dataframe into excel 
    out_df.to_excel(filepath, index=False, startrow=0, startcol=0)

    print("Results printed to excel.")

    return

#--------------------------------------------------------------------------

def print_dict(dict, filepath):
    out_df = pd.DataFrame.from_dict(dict, orient="index")
    out_df.to_excel(filepath)
    print("Print complete.")
    return