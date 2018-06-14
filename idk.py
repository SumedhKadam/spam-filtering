import pandas as pd

com = pd.read_csv('com.csv')

#for i in com['comment']:
print(com['id'].iloc[0])