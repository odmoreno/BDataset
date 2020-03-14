import pandas as pd
import numpy as np

#Leer este post
# https://stackoverflow.com/questions/36226083/how-to-find-which-columns-contain-any-nan-value-in-pandas-dataframe


 
'''

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


'''
#valor1 = dict[key]
          #valor2 = self.p1d[key]
          #key2, link2 = self.getKeyByValue(self.p1d, a1, a2)
          #realvalor = self.p1d[key2]
          #if valor1[0] == valor2[0] and valor1[0] == valor2[0]:
          #    print('coinciden')
          #    freq = int(valor2[2]) + 1
          #    list = [a1, a2, freq]
          #    self.p1d[key] = list


a1 = [('jack', 34, 'Sydney', 155) ,
            ('Riti', 31, 'Delhi' , 177) ,
            ('Mohit', 31,'Delhi' , 167) ,
            ('Veena', 81, 'Delhi' , 144) ,
            ('Shaun', 35, 'Colombo', 111),
            ('Riti', 32, 'Colombo', 111),
            ]

df1 = pd.DataFrame(a1, columns=['Name', 'Age', 'City', 'Marks'])

a2 = [('oscar', 25, 'gye', 155) ,
            ('carlos', 25, 'duran' , 177) ,
            ('Meche', 23,'daule' , 167) ,
            ('Veena', 81, 'Delhi' , 144) ,
            ('Shaun', 35, 'Colombo', 111),
            ('Riti', 32, 'Colombo', 111),
            ]

df2 = pd.DataFrame(a2, columns=['Name', 'Age', 'City', 'Marks'])


key = None

if key == None:
    print('alvv tenia razon')

df=pd.merge(df1,df2,how="outer",indicator=True)
dfleft=df[df['_merge']=='left_only']

dfright=df[df['_merge']=='right_only']
del dfright['_merge']

dboth = df[df['_merge']=='both']

print('test line')


'''
El pozo de funciones

  def compareDf(self, df1, df2, currentD):
    self.get_df_to_compare(df1, df2)
    idf = pd.merge(df1, df2, how='inner')
    #items = currentD.items()
    for index, row in idf.iterrows():
        a1 = row['A1']
        a2 = row['A2']
        key, link= self.getKeyByValue(currentD, a1, a2)
        if self.dictflag:
          valor = link[2] + 1
          list = [a1, a2, valor]
          #tmpD[key] = list
          #logging.info('first: '+ str(list))
          self.p1d[key] = list
        else:
          if key in self.p1d:
              print('Existe la clave: ' + str(key))
              lastvalue = self.p1d[key]
              valor = lastvalue[2] + 1
              list = [link[0], link[1], valor]
              self.check_asambleista(a1, a2, list, lastvalue, currentD, key)
              self.p1d[key] = list
              #logging.info(list)

          else:
              logging.info('No existe registro (Asambleista Nuevo ) :' + str(key))
              valor = link[2]
              list = [link[0], link[1], valor]

              logging.info(list)

              self.check_asambleista(a1, a2, list, valor, currentD, key)

              sizelastd = len(self.p1d)
              self.p1d[sizelastd] = list
              #self.check_asambleista(a1, a2, list , valor, currentD)
              #input("Asambleista nuevo (Press Enter to continue)...")

        currentD[key] = list
        print(currentD[key])
        #logging.info(self.p1d)

    self.dictflag = False
    #input("Comparacion terminada (Press Enter to continue)...")
    print(' NEXT --> ')
    return self.p1d

  def check_asambleista_old(self, a1, a2, list, value, dictActual, key):
      #a1 == 'MORENO INTRIAGO MARIA'
      if a1 == 'PALACIOS CESAR' or a2 == 'PALACIOS CESAR':
          logging.warning('Warn : Se encontro los sgtes asambleistas:  ' + a1 + ' / ' +a2)
          logging.warning(list)
          logging.info('Info: ')
          logging.info(str(value))
          logging.info('Info : diccionario general size: ' + str(len(self.p1d)))
          logging.info(self.p1d[key])
          logging.info('Info : diccionario Actual size' + str(len(dictActual)))
          logging.info(dictActual[key])
          input('Se ENCONTRO AL ASAMBLEISTA!!!! ')
          print(' GO ---<')
      if a1 == 'MORENO INTRIAGO MARIA' or a2 == 'MORENO INTRIAGO MARIA':
          logging.warning('Warn : Se encontro los sgtes asambleistas:  ' + a1 + ' / ' + a2)
          logging.warning(list)
          logging.info(str(value))
          logging.info('Info : diccionario general')
          logging.info(self.p1d)
          logging.info('Info : diccionario Actual')
          logging.info(dictActual)
          input('Se ENCONTRO AL ASAMBLEISTA!!!! ')
          print(' GO ---<')
'''
