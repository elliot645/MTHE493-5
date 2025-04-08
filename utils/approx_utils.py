import json
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.stats import beta

def get_dict_from_json(filepath):
    with open(filepath) as json_file:
        dict = json.load(json_file)
    return dict

# Get total R and B
def get_values(votes, year):
    R = 0
    B = 0
    for county in votes[year]:
        R += votes[year][county]["REPUBLICAN"]
        B += votes[year][county]["DEMOCRAT"]
    return R, B

def plot_weighted_empirical_pdf(votes, year):
    frequency = {}
    total_pop = 0
    for county in votes[year]:
        # get r, b, and ratio
        r = votes[year][county]["REPUBLICAN"]
        b = votes[year][county]["DEMOCRAT"]
        ratio = r/(r+b)
        pop = r+b
        # get frequency of ratio (to nearest hundredth)
        rratio = round(ratio, 2)
        if rratio not in frequency:
            frequency[rratio] = pop
        else:
            frequency[rratio] += pop
        total_pop += pop
    # normalize to get p(u) 
    p = {u:(frequency[u]/total_pop) for u in frequency}
    # plot empirical distribution
    xemp = [u for u in p]
    xemp.sort()
    yemp = []
    for u in xemp:
        yemp.append(p[u])
    plt.plot(xemp, yemp, label="Empirical (Population-Weighted)")
    return

def plot_total_weighted_empirical_pdf(votes):
    frequency = {}
    total_pop = 0
    for year in votes:
        for county in votes[year]:
            if year != '2020':
                # get r, b, and ratio
                r = votes[year][county]["REPUBLICAN"]
                b = votes[year][county]["DEMOCRAT"]
                ratio = round((r/(r+b)), 2)
                pop = r+b
                # get frequency of ratio (to nearest hundredth)
                if ratio not in frequency:
                    frequency[ratio] = pop
                else:
                    frequency[ratio] += pop
                total_pop += pop
    # normalize to get p(u) 
    p = {u:(frequency[u]/total_pop) for u in frequency}
    # plot empirical distribution
    xemp = [u for u in p]
    xemp.sort()
    yemp = []
    for u in xemp:
        yemp.append(p[u])
    plt.plot(xemp, yemp, label="Empirical (Population-Weighted)")
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
    plt.plot(xbeta, ynorm, label="delta="+format(delta, ','))
    return

#=============================================================
# DEPRECATED
#=============================================================

# dataframes = {}
# for endyear in ['2016']:
#     results = {}
#     for state in graphs:
#         network = graphs[state]
#         # get data that won't be altered in trials
#         for node in network:
#             endr = votesdict[endyear][node.id]['REPUBLICAN']
#             endb = votesdict[endyear][node.id]['DEMOCRAT']
#             node.real_ratio = endr/(endr+endb)
#             node.delta = 1
#         # get average error across all trials
#         total_error = 0
#         for trial in range(0,trials):
#             # reset initial conditions
#             for node in network:
#                 node.red = votesdict[startyear][node.id]['REPUBLICAN']
#                 node.blue = votesdict[startyear][node.id]['DEMOCRAT']
#                 node.pop = node.red + node.blue
#             # perform polya process
#             trial_error, total_pop = network_polya(network, timesteps)
#             total_error += trial_error
#         # add to results
#         avg_error = total_error/trials
#         results[podict[state]] = {
#             'Avg Error' : round(avg_error*100,2),
#             'Total Votes' : total_pop
#         }
#         print(state, 'complete.')
#     # create dataframe from results for this year
#     dataframes[endyear] = pd.DataFrame.from_dict(results, orient='index')
#     print(endyear, 'complete.')

# # write to excel sheet
# with pd.ExcelWriter(results_path) as writer:
#     for endyear in dataframes:
#         dataframes[endyear].to_excel(writer, sheet_name=startyear+'-'+endyear)

# # plot county opinion over time for given state
# def plot_opinions(statedict, votesdict, state):
#     years = [2000, 2004, 2008, 2012, 2016, 2020]
#     for county in statedict[state]:
#         opinions = []
#         for year in years:
#             red = votesdict[year][county]["REPUBLICAN"]
#             blue = votesdict[year][county]["DEMOCRAT"]
#             opinion = red/(red+blue)
#             opinions.append(opinion)
#         plt.plot(years, opinions, label=str(red+blue))
#     plt.xlabel("Election Year")
#     plt.ylabel("County Opinion")
#     plt.title("County Opinion vs. Time for" + state)
#     plt.legend()
#     plt.show()
#     return

# def get_data(fipsdict, votesdict, startyear, endyear):
#     data = {}
#     for state in fipsdict:
#         for county in fipsdict[state]:
#             r0 = votesdict[startyear][county]["REPUBLICAN"]
#             b0 = votesdict[startyear][county]["DEMOCRAT"]
#             r1 = votesdict[endyear][county]["REPUBLICAN"]
#             b1 = votesdict[endyear][county]["DEMOCRAT"]
#             pop = r0+b0
#             opinion = r0/(r0+b0)
#             change = abs((r1/(r1+b1))-(r0/(r0+b0)))
#             data[county] = {
#                 "Population" : pop,
#                 "Opinion" : opinion,
#                 "change" : change
#             }
#     return data

# # pass in dict like {fips:{data:int, change:int}}
# def plot_data(data, startyear, endyear, key):
#     xvalues = []
#     yvalues = []
#     for county in data:
#         xvalues.append(data[county][key])
#         yvalues.append(data[county]["change"])
#     plt.scatter(xvalues, yvalues, s=0.5)
#     plt.xlabel("Initial " + key)
#     plt.ylabel("Change in Opinion")
#     plt.title(startyear + "-" + endyear)
#     plt.show()
#     return


# # Plot approximated pdf of U
# def plot_empirical_pmf(votes, year):
#     frequency = {}
#     count = 0
#     for county in votes[year]:
#         # get r, b, and ratio
#         r = votes[year][county]["REPUBLICAN"]
#         b = votes[year][county]["DEMOCRAT"]
#         ratio = r/(r+b)
#         # get frequency of ratio (to nearest hundredth)
#         rratio = round(ratio, 2)
#         if rratio not in frequency:
#             frequency[rratio] = 1
#         else:
#             frequency[rratio] += 1
#         count += 1
#     # normalize to get p(u) 
#     p = {u:(frequency[u]/count) for u in frequency}
#     # plot empirical distribution
#     xemp = [u for u in p]
#     xemp.sort()
#     yemp = []
#     for u in xemp:
#         yemp.append(p[u])
#     plt.plot(xemp, yemp, label="Empirical")
#     return


# # writing to json
# output_path = r'data\countyadj.json'
# with open(output_path, 'w') as file:
#     json.dump(new_adj, file, indent=4)

# # get dict like {state:{fips:county_name}}
# def get_fipsdict_json(filepath):
#     with open(filepath) as json_file:
#         fipsdict = json.load(json_file)
#     return fipsdict

# # get dict like {year:{fips:{party:votes, ..., party:votes}}
# def get_votesdict(filepath):
#     with open(filepath) as json_file:
#         votesdict = json.load(json_file)
#     return votesdict

 # votes_path = r"data\votingdata.json"
    # votes = get_votesdict(votes_path)

    # plot_total_weighted_empirical_pdf(votes)
    # for delta in [4000, 6000, 8000]:
    #     plot_beta_pmf(24000, 12000, delta)
    # plt.show()

    # fignum = 0
    # for year in ['2000', '2004', '2008', '2012', '2016']:
    #     fignum += 1
    #     plt.figure(fignum)
    #     plot_weighted_empirical_pdf(votes, year)
    #     R, B = get_values(votes, year) # total R and B across network
    #     for delta in [5000000, 10000000, 15000000, 20000000]:
    #         plot_beta_pmf(R, B, delta)
    #     plt.xlabel("u")
    #     plt.ylabel("p(u)")
    #     plt.title(year)
    #     plt.legend()
    #     plt.show()

    # for year in ['2000', '2004', '2008', '2012', '2016']:
    #     R, B = get_values(votes, year)
    #     print(year, format(R+B, ','))

    #     # get centrality
    # centrality_dict = {}
    # for state in fipsdict:
    #     # create graph for state
    #     centrality_dict[state] = {}
    #     G = nx.Graph()
    #     for fips in fipsdict[state]:
    #         G.add_node(fips)
    #         G.add_edges_from([(fips, neighbour) for neighbour in adjdict[state][fips]])
            
    #     # calculate centrality for each county
    #     for source in fipsdict[state]:
    #         if len(adjdict[state][source]) > 0:
    #             sum = 0
    #             for target in fipsdict[state]:
    #                 sum += nx.shortest_path_length(G, source, target)
    #             centrality_dict[state][source] = 1/sum
    #         else:
    #             centrality_dict[state][source] = 1

    #     print(state, 'complete.')
    
    # # write to json
    # with open(centrality_path, 'w') as file:
    #     json.dump(centrality_dict, file)