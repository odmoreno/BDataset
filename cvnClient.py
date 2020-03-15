import os
import pandas as pd
import numpy as np
import logging
import csv
import functions
import logging

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
    self.dfflag = True

    self.colsName = ['A1', 'A2', 'valor']
    self.periodos = ['/periodo1', '/periodo2']
    self.lastDf = pd.DataFrame(columns=self.colsName)
    self.p1d = {}
    self.asambleistas = {}

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
      tmpDf = tmpDf.sort_values(by=['periodo', 'sesion', 'titulo'])
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
    logging.info(infotext)
    print(infotext)
    tmpdict = {}
    if mode == 1: 
      tmpdict = self.p1d
    elif mode == 2:
      tmpdict == self.p2d

    pathf = infotext + '.csv'
    count = 1
    for index, row in df.iterrows():
      name = row['titulo'] # Nombre de la sesion
      logging.info('')
      logging.info(' ------------------------- Warn: Votacion ' + name + '--------------------------')
      folderpath = 'datasets/' + name + '.csv'
      currentdf, currentdict = self.validate.create_df(folderpath)
      if self.firstflag:
        self.lastDf = currentdf
        #tmpdict = currentdict
        self.p1d = currentdict
        newfile = 'cv_' + name
        pathtosave = path + newfile + '.csv'
        self.lastDf.to_csv(pathtosave, index = False)
        self.firstflag = False
      else:
       #newdct = self.compareDf(self.lastDf, currentdf, currentdict)
        self.compare_df_v2(self.lastDf, currentdf, currentdict)
        newfile = 'cv_' + name + '.csv'
        pathtosave = path + newfile
        self.writeCsv(self.p1d, pathtosave)
        logging.info('')
        logging.info('_____________________')
        #input(" Save csv (Press Enter to continue)...")


    self.writeCsv(self.p1d, pathf)

  def getKeyByValue(self, dictOfElements, value1, value2):
      listOfItems = dictOfElements.items()
      cod = None
      link = None
      for key, item  in listOfItems:
          if item[0] == value1 and item[1] == value2:
              #print('El codigo es: ' + str(key))
              cod = key
              link = item
              break
      return cod, link

  def get_df_to_compare(self, lastdf, currentdf):

      if self.dfflag:
          del lastdf['valor']
          del currentdf['valor']
          self.dfflag = False
      else:
          del currentdf['valor']

      df = pd.merge(lastdf, currentdf, how="outer", indicator=True)
      dfboth = df[df['_merge']=='both'] # Duplicados para comparar y analizar
      dfright = df[df['_merge']=='right_only'] # Los nuevos del currentdf no incluidos

      del dfright['_merge']
      del dfboth['_merge']
      del df['_merge']
      print('test')
      return df, dfboth, dfright

  def compare_values(self, df):
      for index, row in df.iterrows():
          a1 = row['A1']
          a2 = row['A2']
          key, link = self.getKeyByValue(self.p1d, a1, a2)

          if key == None and link == None:
              print('No existe este conjunto de asambleistas ')
              logging.info('Info Nuevo combinacion de asambleistas: ')
              list = [a1, a2, 1]
              sizelastd = len(self.p1d)
              self.p1d[sizelastd] = list
              logging.info(list)
              #self.check_asambleista(a1, a2, list, sizelastd)
          else:
              print('Coinciden !!!!')
              freq = int(link[2]) + 1
              list = [link[0], link[1], freq]
              self.p1d[key] = list
              #self.check_asambleista(a1, a2, list, key)

  def check_asambleista(self, a1, a2, list, key):
      if a1 == 'PALACIOS CESAR' or a2 == 'PALACIOS CESAR':
          logging.warning('Warn : Se encontro los sgtes asambleistas:  ' + a1 + ' / ' + a2)
          logging.info('Info: ')
          logging.info(list)
          logging.info(self.p1d[key])
          #input('Se ENCONTRO AL ASAMBLEISTA!!!! ')
          #print(' GO ---<')
      if a1 == 'MORENO INTRIAGO MARIA' or a2 == 'MORENO INTRIAGO MARIA':
          logging.warning('Warn : Se encontro los sgtes asambleistas:  ' + a1 + ' / ' + a2)
          logging.info('Info: ')
          logging.info(list)
          logging.info(self.p1d[key])
          #input('Se ENCONTRO AL ASAMBLEISTA!!!! ')
          #print(' GO ---<')

  def compare_df_v2(self, df1, df2, currentDict):
      newdf, inner, right = self.get_df_to_compare(df1, df2)
      self.compare_values(inner)
      self.compare_values(right)
      self.lastDf = newdf

  def writeCsv(self, dict, path):
    tmpdf = pd.DataFrame([], columns=self.colsName)
    items = dict.items()
    for key, link in items:
      tmpdf = tmpdf.append(pd.Series(link, index=self.colsName), ignore_index=True)
    tmpdf.to_csv(path, index=False)
    #with open(path, 'w', encoding ='latin-1', newline='') as file:
    #    writer = csv.writer(file)
    #    items = dict.items()
    #    #writer.writerow(self.colsName)
    #    for key, link in items:
    #        writer.writerow(link)

  def unitTest(self, name):
    'Name, el nombre del csv ha analizar'
    folderpath = 'datasets/' + name + '.csv'
    currentdf, currentdict = self.validate.create_df(folderpath)
    print('Test Line')

if __name__ == '__main__':

    logging.basicConfig(filename='logs/cvns_log.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s %(message)s')
    logger = logging.getLogger('__Cvns__')
    logging.info('------------------------------------------------------------------------------------------')
    logging.info('')
    logging.info('')
    logging.info('Starting')

    client = Covoting()
    client.validate_dir(client.foldername)
    dfp1, dfp2 = client.getdfp(client.pathsesiondf)
    
    #nombre = 'sesion_0_p2_a2017_m05_v3'
    #client.unitTest(nombre)

    client.getcvn(dfp1, 'periodo1', client.path1, mode=1)
    #client.getcvn(dfp2, 'periodo2', client.path2, mode=2)
    
      
    

