import pandas as pd

df = pd.DataFrame({'test':[1,2,3,4], 'test2':[1,2,3,4]}, index=['a','b','c','d'])
df2 = pd.DataFrame({'test':[3, 4, 5, 6], 'test2':[67,2,3,4]}, index=['c','d', 'e', 'f'])



updated = df.index.intersection(df2.index)
added = df2.index.difference(df.index)

df = df2.combine_first(df)
print(df)