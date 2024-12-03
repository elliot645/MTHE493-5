import pandas as pd
import time
import numpy as np

df1 = pd.read_csv('./data/county_pops_2020_to_2023.csv', encoding='latin1')
df2 = pd.read_csv('./data/county_pops_2010_to_2019.csv', encoding='latin1', low_memory = False)
df3 = pd.read_csv('./data/county_pops_2000_to_2009.csv', encoding='latin1', low_memory=False)
for column in df3.columns[6:]:  
            df3[column] = pd.to_numeric(df3[column], errors='coerce')

age_buckets = {
    "0-4": (range(0, 5), ["UNDER5_TOT"]),
    "5-9": (range(5, 10), ["AGE59_TOT"]),
    "10-14": (range(10, 15), ["AGE1014_TOT"]),
    "15-19": (range(15, 20), ["AGE1519_TOT"]),
    "20-24": (range(20, 25), ["AGE2024_TOT"]),
    "25-29": (range(25, 30), ["AGE2529_TOT"]),
    "30-34": (range(30, 35), ["AGE3034_TOT"]),
    "35-39": (range(35, 40), ["AGE3539_TOT"]),
    "40-44": (range(40, 45), ["AGE4044_TOT"]),
    "45-49": (range(45, 50), ["AGE4549_TOT"]),
    "50-54": (range(50, 55), ["AGE5054_TOT"]),
    "55-59": (range(55, 60), ["AGE5559_TOT"]),
    "60-64": (range(60, 65), ["AGE6064_TOT"]),
    "65-69": (range(65, 70), ["AGE6569_TOT"]),
    "70-74": (range(70, 75), ["AGE7074_TOT"]),
    "75-79": (range(75, 80), ["AGE7579_TOT"]),
    "80-84": (range(80, 85), ["AGE8084_TOT"]),
    "85+": (range(85, 101), ["AGE85PLUS_TOT"]),
}

age_buckets_new = {
    1: range(0, 5),
    2: range(5, 10),
    3: range(10, 15),
    4: range(15, 20),
    5: range(20, 25),
    6: range(25, 30),
    7: range(30, 35),
    8: range(35, 40),
    9: range(40, 45),
    10: range(45, 50),
    11: range(50, 55),
    12: range(55, 60),
    13: range(60, 65),
    14: range(65, 70),
    15: range(70, 75),
    16: range(75, 80),
    17: range(80, 85),
    18: range(85, 101),
    }

age_data = {}

def poppy_1(year):
    # Load the dataset
    if year >= 2010 and year < 2020:
        df = df2
    elif year >= 2020 and year < 2024:
        df = df1
    else:
        return

    for col in df.columns[6:]:  # Assuming population-related columns start at index 6
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Process each row of the dataframe
    for index, row in df.iterrows():
        # Extract year and construct FIPS code
        year = row['YEAR']
        state = str(row['STATE']).zfill(2)
        county = str(row['COUNTY']).zfill(3)
        fips = state + county

        # Retrieve or initialize the nested dictionary for the year and FIPS
        year_dict = age_data.setdefault(year, {})
        fips_dict = year_dict.setdefault(fips, {})

        # Process age buckets
        for bucket, (age_range, columns) in age_buckets.items():
            # Aggregate the population for the bucket
            bucket_population = sum(row[col] for col in columns if col in row and pd.notnull(row[col]))

            if bucket_population > 0:
                # Distribute the population uniformly across the ages in the range
                distributed_population = round(bucket_population / len(age_range))

                # Assign population to each age in the range
                for age in age_range:
                    fips_dict[age] = fips_dict.get(age, 0) + distributed_population

    #return age_data

def poppy_2():
    df = df3
    processed = set()
# Process each row in the DataFrame
    for index, row in df.iterrows():
        # Construct the 5-digit FIPS code
        fips = str(int(row['STATE'])).zfill(2) + str(int(row['COUNTY'])).zfill(3)

        # Skip rows where AGEGRP == 0 (aggregate)
        age_group = row['AGEGRP']
        if age_group == 0:
            continue

        # Process each year column for population data
        for year_col in [col for col in df.columns if col.startswith('POPESTIMATE')]:
            year = int(year_col.replace('POPESTIMATE', ''))
            population = row[year_col]

            if pd.notnull(population) and population > 0:

                bucket_key = (year, fips, age_group)
                if bucket_key in processed:
                    continue
                processed.add(bucket_key)


                # Create or retrieve nested dictionaries for year and FIPS
                year_dict = age_data.setdefault(year, {})
                fips_dict = year_dict.setdefault(fips, {})

                # Distribute population uniformly across ages in the bucket
                if age_group in age_buckets_new:
                    ages = age_buckets_new[age_group]
                    distributed_population = round(population / len(ages))

                    for age in ages:
                        fips_dict[age] = fips_dict.get(age, 0) + distributed_population

def get_pop(year):
    if year < 2000 or year > 2023:
        raise ValueError("year must be in range 2000-2023")
    
    if year >= 2010 and year < 2020:
        poppy_1(year)
        year = year - 2007
        population_data = age_data[year]

        return population_data
    elif year >= 2020 and year < 2024:
        poppy_1(year)
        year = year - 2018
        population_data = age_data[year]

        return population_data
    elif year > 1999 and year < 2010:
        poppy_2()
        population_data = age_data[year]

        return population_data

def get_num_votes(voting_df, year):
    
    # Subset to year of interest
    df = voting_df[voting_df["year"] == year]

    # Convert to list of dicts (1 row per dict, keys are columns names)
    data = df.to_dict(orient="records")

    # Create dict to hold votes for each county
    counties = {}

    # Loop through dataset, adding dict of votes for each county
    for row in data:

        if pd.isnull(row['county_fips']):
            continue
        
        county_name = str(int(row['county_fips'])).zfill(5)
        
        if row["party"] == "REPUBLICAN":
            color = "red"
        elif row["party"] == "DEMOCRAT":
            color = "blue"
        else:
            continue

        if county_name not in counties.keys():
            counties[county_name] = {}
        counties[county_name][color] = row['candidatevotes'] + counties[county_name].get(color,0)
        
    return counties

def turnout_dict(year):
    if year < 2000 or year > 2020:
        raise ValueError("year must be in range 2000-2020")
    
    voting_path = "/Users/owen/Desktop/Population_tests/data/countypres_updated copy.csv"
    voting_data = get_num_votes(pd.read_csv(voting_path), year)

    return voting_data

def init_rb(year, county):
    vote_dict = turnout_dict(year)
    pop_dict = get_pop(year)
    
    final_dict = {}

    for county in pop_dict.keys():
        if county not in vote_dict:
            continue

        red_votes = vote_dict[county]['red']
        blue_votes = vote_dict[county]['blue']
        total_votes = red_votes + blue_votes

        if total_votes == 0:
            continue

        sum_pop = 0
        for i in range(0,85):
            sum_pop += pop_dict[county][i]

        # Calculate percentages
        red_percentage = red_votes / sum_pop
        blue_percentage = blue_votes / sum_pop

        # Initialize county in final_dict
        county_dict = final_dict.setdefault(county, {})

        for age in range(0,85): #pop_dict['01001'].keys()

            age_dict = county_dict.setdefault(age, {})

            age_dict['red'] = round(pop_dict[county][age] * red_percentage)
            age_dict['blue'] = round(pop_dict[county][age] * blue_percentage)

    return final_dict[county]


#c = turnout_dict(2000)['Autauga County']
#print(c)

#d = sum(get_pop(2000, 'Alabama', 'Autauga County'))
#print(d)


#print(turnout_dict(2000)['01001'])
#print(get_pop(2000)['01001'])
a = init_rb(2000,'01001')
print(a)
#print(b)

#print('r =', sum(a))
#print('b =',sum(b))

#print(init_colours(2007, '01001'))

#poppy_2()

#print(age_data[2000]['01001'])

#print(age_data[2000]['01001'].keys())

#print(age_data[3]['01001'])

#print(get_pop(2000)['01001'].keys())



    
