import numpy as np
import pandas as pd

def test_dataframe():
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] 

    columns = ['x', 'y', 'z', 'extra']

    df = pd.DataFrame(columns=columns, index=range(5))
    df.loc[0, ['x', 'y', 'z']] = [1, 22, 45]
    df.loc[1, ['x', 'y', 'z']] = [2, 22, 45]
    df.loc[2, ['x', 'y', 'z']] = [3, 22, 45]

    # calculate average sma (2 days)
    df.loc[0:2,'extra'] = df.loc[0:2,"x"].rolling(2).mean()

    # add row and cal again sma
    df.loc[3, ['x', 'y', 'z']] = [4, 22, 45]
    print(df.loc[0:4,"x"].rolling(2).mean())
    #df.loc[[3],'extra'] = df.loc[2:3,"x"].rolling(2).mean()
    print(df)
    print("gg", df.iloc[
                2:4,0].rolling(2).mean())
    print("xx", df.loc[2:3,"x"].rolling(2).mean())
    df.iloc[3:4,3] = df.iloc[
                2:4,0].rolling(2).mean().iloc[1:2]
    print(df)

# outcome of above experiment
# First create empty df of size say 1000
# Then add update multiple records at a time, 
# calculate indicators using previous records 
# and upadte indicators for the current records.