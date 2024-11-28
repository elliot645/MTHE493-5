import pandas as pd

db = pd.read_csv('data/us_county_population_estimates_by_age_2020_to_2023.csv',encoding='latin1')

#print(db.head(10))

# Nested dictionary for population data
age_data = {}

# Defining the age buckets and their corresponding age ranges
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
    "85+": (range(85, 101), ["AGE85PLUS_TOT"]),}

# Process each row
for index, row in db.iterrows():
    year = row.get('YEAR')
    state = row.get('STNAME')
    county = row.get('CTYNAME')

    if not all([year, state, county]):
        continue

    # Create or retrieve nested dictionaries
    year_dict = age_data.setdefault(year, {})
    state_dict = year_dict.setdefault(state, {})
    county_dict = state_dict.setdefault(county, {})

    # Aggregate population for each individual age
    for bucket, (age_range, columns) in age_buckets.items():
        # Total population for the bucket
        bucket_population = sum(row[col] for col in columns if col in row)

        if bucket_population > 0:
            # Distribute the population uniformly across the ages in the range
            distributed_population = round(bucket_population / len(age_range))
            
            # Assign to individual ages
            for age in age_range:
                county_dict[age] = county_dict.get(age, 0) + distributed_population


#years: 1 = 4/1/2020, 2 = 7/1/2020, 3 = 7/1/2021, 4 = 7/1/2022, 5 = 7/1/2023
def get_population_data(year, state, county):
    #return a dictionary of the form data[state][county] that returns a population list for that county
    if year > 2018:
        year -= 2018 #just so we can ref years directly (wrong for 4/1/2020)
    population_data = []
    for i in range(0,101):
        population_data.append(age_data[year][state][county][i])
    return population_data

print(get_population_data(1, 'Alabama', 'Autauga County'))