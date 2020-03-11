import pandas as pd
import numpy as np
import csv

class Validate:

  def __init__(self):

    self.nanFlag = False
    self.votos = ['SI', 'NO', 'BLANCO', 'ABSTENCION', 'AUSENTE']
    self.colsName = ['A1', 'A2', 'valor', 'voto']
    self.nombresOlvidados = []

  def validate_nans(self, df):
    #df.dropna(inplace=True)
    dftmp = df[df.isnull().any(axis=1)]
    #print(dftmp)
    nombre = ''
    if dftmp.size > 0 :
      #print('Hay nan ')
      for index, row in dftmp.iterrows():
        cols = row.axes[0]
        row1 = cols[0] #puedes ser curul o curulasambleista
        row2 = None
        if row1 == 'Curul Asambleista':
          row2 = cols[1] # la sgte sera la columna del voto
          curulAsam = row[row1]
          voto = row[row2]
          if pd.isnull(curulAsam):
            #print('Test: Hay nan')
            pass
          if ( not pd.isnull(curulAsam) and pd.isnull(voto)):
            print('Hay nans en voto, pero no en curulAsam')
            nombre = nombre + ' ' + curulAsam
            self.nanFlag = True

      if self.nanFlag:
        self.nombresOlvidados.append(nombre)
        self.nanFlag = False

      df.dropna(inplace=True)
      #print(' NANS: ' + nombre)
      
    return df

  def validate_num_col(self, value):
    value = str(value)
    size = len(value)
    num = ''
    name = ''
    if(size <= 2):
      print('Falta el nombre: ')
      print(self.nombresOlvidados)
      v1 = value[0]
      v2 = v1 + value[1]
      num = v2
      name = self.nombresOlvidados[0]
      self.nombresOlvidados.pop(0)
      return num, name
    else:
      v1 = value[0]
      v2 = v1 + value[1]
      v3 = v2 + value[2]
    if v1.isdigit():
      if v2.isdigit():
        if v3.isdigit():
          num = v3
          name = value[4:]
        else:
          num = v2
          name = value[3:]
      else:
        num = v1
        name = value[2:]
    return num, name

  def validate_rows(self, df):
    #print(df)
    cols = ['curul', 'asambleista', 'voto']
    dfcols = df.columns.values
    df.columns = map(str.lower, df.columns)
    dfcols = [x.lower() for x in dfcols]
    s = set(dfcols)
    #matches = [j for i, j in zip(cols, dfcols) if i != j]
    matches = [x for x in s if x not in cols]
    matches = [y.lower() for y in matches]
    #print('matches: ')
    #print(matches)
    curul = []
    asambleista = []
    if len(matches) > 0:
      #print('Errores en columnas')
      nameErr = 'curul asambleista'
      if nameErr in matches:
        #print('contains curul asambleista')
        values = df[nameErr].tolist()
        for value in values:
          v1, v2 = self.validate_num_col(value)
          curul.append(v1)
          asambleista.append(v2)

        df['curul'] = curul
        df['asambleista'] = asambleista
        del df[nameErr]

      #print(df)
    return df
  
  def validate_df(self, df):
    dfcols = df.columns.values
    nro = dfcols[0]
    print('columna: ' + nro)
    tmp = df.drop(columns=nro)
    tmp = tmp.loc[:, ~tmp.columns.str.contains('^Unnamed')]
    tmp = self.validate_nans(tmp)
    tmp = self.validate_rows(tmp)
    return tmp


  def create_df(self, pathSesion):
    votos = ['SI', 'NO', 'BLANCO', 'ABSTENCION', 'AUSENTE']
    colsName = ['A1', 'A2', 'voto', 'valor']

    df = pd.read_csv(pathSesion)
    df = df[['asambleista', 'curul', 'voto']]

    colVotos = df['voto']
    tmpDf = pd.DataFrame(columns=colsName)

    dict = {}
    count = 0
    for voto in votos:
      if voto in colVotos.values:
        votoDf = df.loc[df['voto'] == voto]
        lol = votoDf.values.tolist()
        for index, this in enumerate(lol):
          for that in lol[index + 1:]:
            info = [this[0], that[0], this[2], 1]
            tmpDf = tmpDf.append(pd.Series(info, index=colsName), ignore_index=True)
            dict[count] = info
            count +=1
            #print('this: ' + this[0] + ' that: ' + that[0])
        #print(tmpDf)
      else:
        print('No hay votos con: ' + voto)

    return tmpDf, dict

  def create_zeros(self, df, tam):

    for i in range(0, tam):
      tmp = pd.DataFrame({"A1": 'test', "A2": 'test', "voto": 'test', "valor": [0]})
      df = df.append(tmp, ignore_index=True)

    return df

  def get_asunto(self, info, indice, periodo, mes):
    fechaFlag = False
    sesionFlag = False
    lockSesion = False
    totalFlag = False
    presenteFlag =False
    ausenteFlag = False
    siFlag = False
    noFlag = False
    blancoFlag = False
    abstencionFlag = False
    #Datos
    sesion= 0
    asunto= ''
    fecha = ''
    hora = ''
    total = 0
    presente = 0
    ausente = 0
    si = 0
    no = 0
    blanco = 0
    abstencion = 0
    values = []
    for text in info:
      text = text.lower()
      if sesionFlag == True and fechaFlag == False:
        asunto = asunto + text + ' '
        #print(asunto)
      if ("sesión" in text) and lockSesion == False:
        #print(text)
        sesion = [int(s) for s in text.split() if s.isdigit()]
        sesion = str(sesion[0])
        #print(sesion[0])
        sesionFlag = True
        lockSesion = True
      if fechaFlag:
        fecha = text
        fecha = fecha[:-5]
        #print(fecha)
        hora = text[-5:]
        #print(hora)
        fechaFlag = False
      if "votación definitiva" in text:
        #print('La sgte contiene la fecha')
        sesionFlag = False
        fechaFlag = True
      if totalFlag:
        total = int(text)
        totalFlag = False
      if presenteFlag:
        presente = int(text)
        presenteFlag = False
      if ausenteFlag:
        ausente = int(text)
        ausenteFlag = False
      if siFlag:
        si = int(text)
        siFlag = False
      if noFlag:
        no = int(text)
        noFlag = False
      if blancoFlag:
        blanco = int(text)
        blancoFlag = False
      if abstencionFlag:
        abstencion = int(text)
        abstencionFlag = False
      if text == "total": totalFlag = True
      if text == "presente": presenteFlag = True
      if text == "ausente": ausenteFlag = True
      if text == "si": siFlag = True
      if text == "no": noFlag = True
      if text == "blanco": blancoFlag = True
      if text == "abstencion": abstencionFlag = True

    sesionName = 'sesion'+ '_' + sesion + '_p' + str(periodo) + '_m' + str(mes) +'_v' + str(indice)
    values.append(sesionName), values.append(periodo), values.append(sesion), values.append(indice), values.append(fecha), values.append(hora), values.append(total), values.append(presente), values.append(ausente)
    values.append(si), values.append(no), values.append(blanco), values.append(abstencion), values.append(asunto)
    print(values)

    return sesionName, values
