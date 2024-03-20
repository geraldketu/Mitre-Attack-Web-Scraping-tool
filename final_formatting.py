import pandas as pd


df = pd.read_csv('data.csv')


print("Original column names:")

df.columns = ['ID', 'Name', 'Description']

df['Description'] = df['Description'].str.replace('\[.*?\]', '', regex=True)


df.to_csv("MitreAttack_Techniques_DataSet.csv", index=False)


print(df.head())
