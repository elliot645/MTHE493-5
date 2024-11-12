#Data Collected from https://www.census.gov/data/tables/time-series/demo/popest/2020s-counties-detail.html

import pandas as pd

db = pd.read_csv('data/us_county_population_estimates_by_age_2020_to_2023.csv',encoding='latin1')


print(db.head(10))