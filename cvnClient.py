import os
import pandas as pd
import numpy as np
import logging
import csv
import functions

from os import path, getcwd, makedirs

class Covoting:

  def __init__(self):

    self.validate = functions.Validate()
    self.tmpsesiondf = 'tmpSesiones.csv'
    self.pathsesiondf = 'sesiones.csv'
    
    self.foldername = 'cvnetworks/'
    self.path1 = 'cvnetworks/periodo1/'
    self.path2 = 'cvnetworks/periodo2/'

    self.firstflag = True
    self.dictflag = True

    self.colsName = ['A1', 'A2', 'voto', 'valor']
    self.periodos = ['/periodo1', '/periodo2']
    self.lastDf = pd.DataFrame(columns=self.colsName)
    self.p1d = {}
    self.p2d = {}

  def validate_dir(self,path):
    if not os.path.exists(path):
      makedirs(path)
      makedirs(self.path1)
      makedirs(self.path2)

  def getdfp(self, pathdf, flag=True):
    'Obtiene los Dataframes por periodo'
    if flag:
      sesionDf = pd.read_csv(pathdf)
      tmpDf = sesionDf
      tmpDf = tmpDf.sort_values(by=['periodo', 'titulo'])
      print(tmpDf)
      print('testline')
      path = 'tmpSesiones.csv'
      tmpDf.to_csv(path, index=False)
    else:
      sesionDf = pd.read_csv(self.tmpsesiondf)
      tmpDf = sesionDf
    
    dfp1 = tmpDf.loc[tmpDf['periodo'] == 1]
    dfp2 = tmpDf.loc[tmpDf['periodo'] == 2]
    print('test line')
    return dfp1, dfp2
  
  def getcvn(self, df, infotext, path, mode = 1):
    'Recive el dataframe (df) para leer los csv de sesiones para luego convertirlos en dict y cvnetwork.csv'
    print(infotext)
    tmpdict = {}
    if mode == 1: 
      tmpdict = self.p1d
    elif mode == 2:
      tmpdict == self.p2d

    count = 1
    for index, row in df.iterrows():
      name = row['titulo'] # Nombre de la sesion
      #newfile = 'cv_' + name
      #pathtosave = path + newfile + '.csv'
      #if not os.path.exists(pathtosave):
      folderpath = 'datasets/' + name + '.csv'
      currentdf, currentdict = self.validate.create_df(folderpath)
      #if count >=num:
      #    print('Finish test!! ')
      #    break
      if self.firstflag:
        self.lastDf = currentdf
        #tmpdict = currentdict
        self.p1d = currentdict
        newfile = 'cv_' + name
        pathtosave = path + newfile + '.csv'
        self.lastDf.to_csv(pathtosave, index = False)
        self.firstflag = False
      else:
        newdct = self.compareDf(self.lastDf, currentdf, currentdict)
        self.lastDf = currentdf
        newfile = 'cv_' + name + '.csv'
        pathtosave = path + newfile
        self.writeCsv(newdct, newfile, pathtosave)

      count += 1
    

  
  def getKeyByValue(self, dictOfElements, value1, value2):
      listOfItems = dictOfElements.items()
      cod = 0 
      link = None
      for key, item  in listOfItems:
          if item[0] == value1 and item[1] == value2:
              print('El codigo es: ' + str(key))
              cod = key
              link = item
              break
      return cod, item
        
  def compareDf(self, df1, df2, currentD):
    idf = pd.merge(df1, df2, how='inner')
    #items = currentD.items()
    for index, row in idf.iterrows():
        a1 = row['A1']
        a2 = row['A2']
        key, link= self.getKeyByValue(currentD, a1, a2)
        if self.dictflag:
          valor = link[3] + 1
          list = [a1, a2, link[2], valor]
          #tmpD[key] = list
          self.p1d[key] = list
        else:
          if key in self.p1d:
              print('Existe la clave: ' + str(key))
              lastvalue = self.p1d[key]
              valor = lastvalue[3] + 1
              list = [link[0], link[1], link[2], valor]
              #tmpD[key] = list
              self.p1d[key] = list
          else:
              print('No existe registro: ' + str(key))
              valor = link[3]
              list = [link[0], link[1], link[2], valor]
              sizelastd = len(self.p1d)
              #tmpD[sizelastd] = list
              self.p1d[sizelastd] = list

        currentD[key] = list
        print(currentD[key])

    self.dictflag = False
    print('test line')
    return self.p1d

  def writeCsv(self, dict, name, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        items = dict.items()
        writer.writerow(self.colsName)
        for key, link in items:
            writer.writerow(link)

  def unitTest(self, name):
    'Name, el nombre del csv ha analizar'
    folderpath = 'datasets/' + name + '.csv'
    currentdf, currentdict = self.validate.create_df(folderpath)
    print('Test Line')

if __name__ == '__main__':
    
    client = Covoting()
    #client.validate_dir(client.foldername)
    #dfp1, dfp2 = client.getdfp(client.pathsesiondf)
    
    nombre = 'sesion_0_p2_a2017_m05_v1'
    client.unitTest(nombre)

    client.getcvn(dfp1, 'Sesiones del primer (1) periodo', client.path1, mode=1)
    #client.getcvn(dfp2, 'Sesiones del primer (2) periodo', client.path2, 12, mode=2)
    
      
    

