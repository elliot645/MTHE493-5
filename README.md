# MTHE493-5

### Instructions
Run the main file to run the simulation

### Structure of the model
- Main File
    - Define state and period of interest
    - Build graph
        - Connect Nodes using adjacency matrix function
        - Initialize red and blue counts using past voting data
        - Initialize population lists using population data
    - Visualize graph before simulation
    - Run polya simulation. At each step, do the following:
        - Pick a ball from the urn's (county's) super urn
        - x = number of people who turned 18 that day (becoming eligible voters)
        - Add x more balls of the chosen color
        - Use immigration function to determine how many balls to add or remove
    - Visualize graph after simulation

