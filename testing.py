import pandas as pd
import csv

data = {
    '00': {'00': 1, '01': 2, '11': 3},
    '01': {'00': 4, '01': 5, '11': 6},
    '11': {'00': 7, '01': 8, '11': 9},
}

#GO FROM DICT OF DICT TO CSV
df = pd.DataFrame.from_dict(data, orient="index")
df.to_csv('dict_testing.csv')

#GO FROM CSV TO DICT OF DICTS
df2 = pd.read_csv('dict_testing.csv', dtype=str)  # Read the entire file as strings
df2.set_index(df2.columns[0], inplace=True)  # Set the first column as the index

df2 = df2.apply(pd.to_numeric)

data2 = df2.to_dict(orient="index")

print(data['01'].values())
print(data2['01'].values())




