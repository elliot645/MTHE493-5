
"""

1. Initialize global objects
    a. Adjacency matrix
    b. Voting data
2. Run model on every state for a year (e.g. run_model(adjacency_matrix, voting_data, year))
2. Run model on various states/years (e.g. run_model(ajdacency_matrix, voting_data, state, year))
    a. Get initial and final voting data
    b. Initialize graph
    c. Run polya process
    d. Quantify accuracy
        i. Ratio by county:

            ratios = {
                county: { 
                    start: {ratio:, total_votes: }
                    real: {ratio: , total_votes: }
                    model: {ratio: , total_votes: }
                }
            }

        ii. Accuracy:

            accuracy = {
            county : 
            }

                

"""