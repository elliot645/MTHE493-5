import pandas as pd
import time


def get_df(year):
    if year >= 2020 and year <= 2023:
        db = pd.read_csv('./data/us_county_population_estimates_by_age_2020_to_2023.csv', encoding='latin1')
    elif year >= 2010 and year < 2020:
        db = pd.read_csv('./data/CC-EST2020-AGESEX-ALL.csv', encoding='latin1', low_memory = False)
        for column in db.columns[6:]:  
            db[column] = pd.to_numeric(db[column], errors='coerce')
    elif year >= 2000 and year < 2010:
        db = pd.read_csv('./data/co-est00int-agesex-5yr.csv', encoding='latin1', low_memory=False)
        for column in db.columns[6:]:  
            db[column] = pd.to_numeric(db[column], errors='coerce')
    else:
        raise ValueError("Year must be in range 2000-2023")
    return db
    
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

def pop_1(year):
    if year >= 2010 and year < 2020:
        df = get_df(2011)
    elif year >= 2020 and year < 2024:
        df = get_df(2021)
    else:
        return
    
    for index, row in df.iterrows():
        year = row.get('YEAR')
        state = row.get('STNAME')
        county = row.get('CTYNAME')

        if not all([year, state, county]):
            continue  # Skip rows with missing key identifiers

        # Create or retrieve nested dictionaries
        year_dict = age_data.setdefault(year, {})
        state_dict = year_dict.setdefault(state, {})
        county_dict = state_dict.setdefault(county, {})

        # Aggregate population for each individual age
        for bucket, (age_range, columns) in age_buckets.items():
            # Total population for the bucket
            bucket_population = sum(row[col] for col in columns if col in row and pd.notnull(row[col]))

            if bucket_population > 0:
                # Distribute the population uniformly across the ages in the range
                distributed_population = round(bucket_population / len(age_range))
                
                # Assign to individual ages
                for age in age_range:
                    county_dict[age] = county_dict.get(age, 0) + distributed_population

def pop_2():
    df = get_df(2002)
    for index, row in df.iterrows():
        # Retrieve identifiers
        state = row.get('STNAME')
        county = row.get('CTYNAME')
        age_group = row.get('AGEGRP')
        sex = row.get('SEX')

        # We focus only on total population (SEX == 0) and exclude aggregate AGEGRP == 0
        if sex != 0 or age_group == 0:
            continue

        # Iterate through population estimate columns (2000-2010)
        for year_col in [col for col in df.columns if col.startswith('POPESTIMATE')]:
            year = int(year_col.replace('POPESTIMATE', ''))
            population = row.get(year_col, 0)
            
            if pd.notnull(population) and population > 0:
                # Create or retrieve nested dictionaries
                year_dict = age_data.setdefault(year, {})
                state_dict = year_dict.setdefault(state, {})
                county_dict = state_dict.setdefault(county, {})

                # Distribute population across individual ages in the bucket
                if age_group in age_buckets_new:
                    ages = age_buckets_new[age_group]
                    distributed_population = round(population / len(ages))

                    for age in ages:
                        county_dict[age] = county_dict.get(age, 0) + distributed_population

def get_pop(year, state, county):
    if year < 2000 or year > 2023:
        raise ValueError("year must be in range 2000-2023")
    population_data = []
    if year >= 2010 and year < 2020:
        pop_1(year)
        year = year - 2007
        for i in range(0,101):
            population_data.append(age_data[year][state][county][i])
        return population_data
    elif year >= 2020 and year < 2024:
        pop_1(year)
        year = year - 2018
        for i in range(0,101):
            population_data.append(age_data[year][state][county][i])
        return population_data
    elif year > 1999 and year < 2010:
        pop_2()
        for i in range(0,101):
            population_data.append(age_data[year][state][county][i])
        return population_data

st = time.time()*1000
print(get_pop(2000, 'Alabama', 'Autauga County'))
end = time.time()*1000
print(f"Time to generate list: {int(end-st)}ms")