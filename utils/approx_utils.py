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

#=============================================================
# ARCHIVE
#=============================================================

# plot county opinion over time for given state
def plot_opinions(statedict, votesdict, state):
    years = [2000, 2004, 2008, 2012, 2016, 2020]
    for county in statedict[state]:
        opinions = []
        for year in years:
            red = votesdict[year][county]["REPUBLICAN"]
            blue = votesdict[year][county]["DEMOCRAT"]
            opinion = red/(red+blue)
            opinions.append(opinion)
        plt.plot(years, opinions, label=str(red+blue))
    plt.xlabel("Election Year")
    plt.ylabel("County Opinion")
    plt.title("County Opinion vs. Time for" + state)
    plt.legend()
    plt.show()
    return

def get_data(fipsdict, votesdict, startyear, endyear):
    data = {}
    for state in fipsdict:
        for county in fipsdict[state]:
            r0 = votesdict[startyear][county]["REPUBLICAN"]
            b0 = votesdict[startyear][county]["DEMOCRAT"]
            r1 = votesdict[endyear][county]["REPUBLICAN"]
            b1 = votesdict[endyear][county]["DEMOCRAT"]
            pop = r0+b0
            opinion = r0/(r0+b0)
            change = abs((r1/(r1+b1))-(r0/(r0+b0)))
            data[county] = {
                "Population" : pop,
                "Opinion" : opinion,
                "change" : change
            }
    return data

# pass in dict like {fips:{data:int, change:int}}
def plot_data(data, startyear, endyear, key):
    xvalues = []
    yvalues = []
    for county in data:
        xvalues.append(data[county][key])
        yvalues.append(data[county]["change"])
    plt.scatter(xvalues, yvalues, s=0.5)
    plt.xlabel("Initial " + key)
    plt.ylabel("Change in Opinion")
    plt.title(startyear + "-" + endyear)
    plt.show()
    return