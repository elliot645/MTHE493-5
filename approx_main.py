from utils.approx_utils import *
from utils.polya_utils import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
from scipy.stats import beta
import pandas as pd

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

# plot Beta distribution of an urn
def plot_beta_pdf(R, B, deltas):
    for delta in deltas:
        x = np.linspace(beta.ppf(0.01, (R/delta), (B/delta)), beta.ppf(0.99, (R/delta), (B/delta)), 100)
        plt.plot(x, beta.pdf(x, (R/delta), (B/delta)), label=delta)
    plt.xlabel("ratio of red u")
    plt.ylabel("f(U=u)")
    plt.legend()
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


if __name__ == "__main__":

    fips_path = r"data\statefips.json"
    votes_path = r"data\votingdata.json"
    adj_path = r"data\county_adjacency.csv"

    state = "NH"
    startyear = 2000
    endyear = 2004
    timesteps = 10000

    fipsdict = get_fipsdict(data_path, fips_sheet, state)    # Nodes
    neighbours = get_adjacency_dict(adj_path, fipsdict)      # Edges
    network = Graph()                                        #
    network.set_topology(fipsdict, neighbours)
    vdf = get_df(data_path, votes_sheet)                     #
    startvotes = get_votes(vdf, fipsdict, startyear, state)
    endvotes = get_votes(vdf, fipsdict, endyear, state)

    # initialize nodes with R, B, delta

    # run Polya process
    




    """
    Observations

    Model 1: Generalistic
        -observe that variance (i.e. delta) is larger for counties closer to 50/50
        -delta=f(R,B)
        -try to identify which 50/50 counties more likely to swing; investigate trends:
            -population
            -geography
            -centrality (urban/rural)
            -direction of swing
        -evaluate error & tune the delta function according to findings 
            (e.g. delta=f(R, B, population, centrality))

    Model 2: Backward-Looking
        -set delta according to change in opinion
            e.g. delta= K|U_f - U_i| for some constant K
        -likelihood to swing depends on magnitude of real-life swing
        -tune similary to model 1
    """





    

    





    

            
