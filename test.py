import pandas as pd
import numpy as np

#Leer este post
# https://stackoverflow.com/questions/36226083/how-to-find-which-columns-contain-any-nan-value-in-pandas-dataframe


# List of Tuples
empoyees = [('jack', 34, 'Sydney', 155) ,
            ('Riti', 31, 'Delhi' , 177) ,
            (np.nan, np.nan, 'Mumbai', 81) ,
            ('Mohit', 31,'Delhi' , 167) ,
            ('Veena', 81, 'Delhi' , 144) ,
            ('Shaunak', np.nan, 'Mumbai', 135 ),
            ('Shaun', 35, 'Colombo', 111),
            ('Riti', 32, 'Colombo', 111),
            ]
 
# Create a DataFrame object
df = pd.DataFrame(empoyees, columns=['Name', 'Age', 'City', 'Marks'])
 
print('Contents of the dataframe :')
print(df)

cols = df.columns.values
print(cols)

nancol = df.columns[df.isna().any()].tolist()
print(nancol)

dftmp = df[df.isnull().any(axis=1)]
print(dftmp)

for index, row in dftmp.iterrows():
  z = row.axes[0]
  size = len(z)
  beb = z[1]
  a = str(row['Name'])
  b = row['Age']
  c = row['City']
  d = row['Marks']
  if a.lower() == 'nan':
    print('Es un NaN D:!')



#Not nan or null columns
tmp = df[df.columns[~df.isna().any()]]
print(tmp)

notnan = df.columns[~df.isna().any()].tolist()
print(notnan)

print('test line')