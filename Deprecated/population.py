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

print(get_population_data(1, 'Alabama', 'Autauga County'))