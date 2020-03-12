from tabula import read_pdf
import pandas as pd
import fitz
import os

import functions

#from funciones import validate_df, get_asunto

class ADataset:

  def __init__(self):
    self.basedir = 'datasets/' #current base dir
    self.pdfdir = None
    self.curulFlag = False
    self.mixFlag = False
    self.sesionName = ''
    self.validate = functions.Validate()
    self.meses = ['01', '02', '03', '04','05', '06', '07', '08', '09', '10', '11', '12']

  def get_dfs(self):
    ''' Obtener las tablas como dataframes'''
    df = read_pdf(self.pdfdir, multiple_tables=True, pages="all") # Obtiene las tablas del pdf como dateframes
    #tmp = df[0] #Informacion general del resumen de la votacion
    #print(tmp)
    df = df[1:] #Eliminamos el resumen de la votacion
    df = df[:-1] # Eliminamos la ultima columna que representa el total presente
    return df

  def concat_dfs(self, list):
    current_df = list[0] #obtenemos la primera tabla
    #current_df = self.validate_df(current_df)
    current_df = self.validate.validate_df(current_df)
    #current_df = current_df[:-1] #Eliminamos la ultima fila, que representa el total de tal opcion de votacion
    tmp = list[1:] # Como tenmos la primera tabla, no la necesitamos mas y la descartamos
    df = None
    for element in tmp:
      #element = element[:-1] #Elimina ultima fila
      #element = self.validate_df(element)
      element = self.validate.validate_df(element)
      df = pd.concat([current_df, element], axis=0, ignore_index=True)
      current_df = df
      #print(df)
    return  df

  def get_csv(self, df, name):
    #tmp = df.drop(columns="nro.")
    #print(tmp)
    path = self.basedir + name + '.csv'
    df.to_csv(path, index=False)
  
  def get_info(self, indice, age, month):
    doc = fitz.open(self.pdfdir)
    #print("number of pages: %i" % doc.pageCount)
    #print(doc.metadata)
    page1 = doc.loadPage(0) #Resumen de la votacion
    page1text = page1.getText("text")
    info = page1text.split("\n")
    info = info[1:]
    periodo = None
    if age >= '2017':
      periodo = 2
    else: 
      periodo = 1
    
    mes = self.get_month(month)
    name, values = self.validate.get_asunto(info, indice, periodo, age , mes)
    self.sesionName = name

    return values

  def get_month(self, mes):
    valor = ''
    mes = mes.lower()
    mes = mes.strip()
    if mes == 'enero':
      valor = self.meses[0]  
    elif mes == 'febrero':
      valor = self.meses[1]
    elif mes == 'marzo':
      valor = self.meses[2]
    elif mes == 'abril':
      valor = self.meses[3]
    elif mes == 'mayo':
      valor = self.meses[4]
    elif mes == 'junio':
      valor = self.meses[5]
    elif mes == 'julio':
      valor = self.meses[6]
    elif mes == 'agosto':
      valor = self.meses[7]
    elif mes == 'septiembre':
      valor = self.meses[8]
    elif mes == 'octubre':
      valor = self.meses[9]
    elif mes == 'noviembre':
      valor = self.meses[10]
    elif mes == 'diciembre':
      valor = self.meses[11]
    else:
      valor = 'none'
    return valor


  def write_info(self, info):
    path = self.basedir + 'info1.txt'
    with open(path, "w") as output:
      for row in info:
        output.write(str(row) + '\n')
  
  def main(self, indice):
    dfs = self.get_dfs()
    dfconcat = self.concat_dfs(dfs)
    info = self.get_info(indice, '2013')
    print(info)
    
    self.get_csv(dfconcat, self.sesionName)
    #self.get_csv(dfconcat)
    #self.write_info(info)

  def validate_dir(self,path):
    if not os.path.exists(path):
      os.makedirs(path)

  def validate_last_row(self, df):
    last = df[-1:]
    #print(cols)
    val = last.values
    val1 = str(val[0][1])
    val2 = str(val[0][3])
    if (val1.lower() == 'nan' ) or (val2.lower() == 'nan'):
      df = df[:-1]

    return df


if __name__ == '__main__':
    
    client = ADataset()
    #client.basedir = '/datasets/'
    client.validate_dir(client.basedir)

    indice = 0 
    #folder = 'pdfs/Año 2017/Mayo 2017/Votaciones de la Sesión de instalación de la Asamblea Nacional 2017-2021/'
    #namepdf = 'Sesión de instalación de la Asamblea Nacional 2017-2021 - Elección Libia Rivas Secretaria General.pdf'
    folder = 'pdfs/Año 2013/Julio/Sesión 197 del Pleno continuación (23-07-2013)/'
    namepdf = '2- Sesión 197 continuación Legalización de Terre.pdf'
    path = folder + namepdf

    client.pdfdir = path
    #client.pdfdir = '1- Sesión 215 del Pleno Archivo de los Proyectos de Ley de Reforma a la Ley Orgánica del Servicio Público.pdf'
    client.main(indice)
    
