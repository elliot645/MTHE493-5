import pandas as pd


"""Note:don't have data by county (yet) so will have to evaluate accuracy by district; will not be able to evaluate
years where the state was redistricted (e.g. 2020 for Florida)"""

"""ASSUMPTION: any votes not cast for the winner were cast for the opposite party (i.e. excluding communist/independent/etc candidates)"""
def historical_ratio (filepath):

    # Read file into datafram - only read desired year? Or filter after 
    df = pd.read_excel(...)

    # Convert dataframe to list of dicts: 
    records = df.to_dict(orient='records')

    # Filter

    # Calculate ratio for each district

    # Calculate average U

    # Return vector of ratios and average U

    return 


if __name__ == "__main__":

    path = "..."
    historical_ratio(path)