from utils.approx_utils import *
from utils.polya_utils import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
from scipy.stats import beta
import pandas as pd

# Get total R and B
def get_values(votes, year):
    R = 0
    B = 0
    for county in votes[year]:
        R += votes[year][county]["REPUBLICAN"]
        B += votes[year][county]["DEMOCRAT"]
    return R, B

# Plot approximated pdf of U
def plot_empirical_pmf(votes, year):
    frequency = {}
    count = 0
    for county in votes[year]:
        # get r, b, and ratio
        r = votes[year][county]["REPUBLICAN"]
        b = votes[year][county]["DEMOCRAT"]
        ratio = r/(r+b)
        # get frequency of ratio (to nearest hundredth)
        rratio = round(ratio, 2)
        if rratio not in frequency:
            frequency[rratio] = 1
        else:
            frequency[rratio] += 1
        count += 1
    # normalize to get p(u) 
    p = {u:(frequency[u]/count) for u in frequency}
    # plot empirical distribution
    xemp = [u for u in p]
    xemp.sort()
    yemp = []
    for u in xemp:
        yemp.append(p[u])
    plt.plot(xemp, yemp, label="Empirical")
    return
    
# Plot beta distribution of U
def plot_beta_pmf(R, B, delta):
    # xbeta = np.linspace(beta.ppf(0.01, (R/delta), (B/delta)), beta.ppf(0.99, (R/delta), (B/delta)), 84)
    xbeta = np.linspace(0, 1, 84)
    ybeta = (beta.pdf(xbeta, (R/delta), (B/delta)))
    ysum = sum(ybeta)
    ynorm = []
    for y in ybeta:
        ynorm.append(y/ysum)
    plt.plot(xbeta, ynorm, label="delta="+str(delta))
    return

#-------------------------------------------------------

if __name__ == "__main__":
    
    votes_path = r"data\votingdata.json"
    votes = get_votesdict(votes_path)

    year = '2008'
    plot_empirical_pmf(votes, year)
    R, B = get_values(votes, year)      # sum of all r and b; superurn r and b for a complete network
    for delta in [9000000, 10000000, 11000000]:
        plot_beta_pmf(R, B, delta)

    plt.xlabel("u")
    plt.ylabel("p(u)")
    plt.title(year)
    plt.legend()
    plt.show()
    









    

    





    

            
