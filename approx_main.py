from utils.approx_utils import *
from utils.polya_utils import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
from scipy.stats import beta

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
    plt.show()
        
# plot error over time 
# delta is a node attribute
def plot_error(graph, T=1000):
    pass

if __name__ == "__main__":

    fips_path = r"data\statefips.json"
    votes_path = r"data\votingdata.json"

    # plot error for delta=1

    # plot error for delta = f(change in U)

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





    

    





    

            
