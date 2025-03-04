from campaign_main import *

# get dict like {state:{fips:county_name}}
def get_fipsdict_json(filepath):
    with open(filepath) as json_file:
        fipsdict = json.load(json_file)
    return fipsdict

# get dict like {year:{fips:{party:votes, ..., party:votes}}
def get_votesdict(filepath):
    with open(filepath) as json_file:
        votesdict = json.load(json_file)
    return votesdict
