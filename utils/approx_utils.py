from campaign_main import *

# get dict like {state:{fips:county_name}}
def get_statedict(filepath):
    with open(filepath) as json_file:
        stringdict = json.load(json_file)
    statedict = {state:{} for state in stringdict}
    for state in statedict:
        for fips in stringdict[state]:
            statedict[state][int(fips)] = stringdict[state][fips]
    return statedict

# get dict like {year:{fips:{party:votes, ..., party:votes}}
def get_votesdict(filepath):
    with open(filepath) as json_file:
        stringdict = json.load(json_file)
    votesdict = {int(year):{} for year in stringdict}
    for year in votesdict:
        for fips in stringdict[str(year)]:
            votesdict[year][int(fips)] = stringdict[str(year)][fips]
    return votesdict
