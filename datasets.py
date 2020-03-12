import os
import pandas as pd
import logging

import csvClient

class BDataset:

  def __init__(self):
    self.pdfsfolder = '/home/ubuntu/Documents/B1/B3/pdfs/'
    self.basedir = 'datasets/'
    self.csv = csvClient.ADataset()
    self.currentsession = ''
    self.indiceName = 'sesiones.csv'
    self.currentAge = ''
    self.currentMonth = ''
    self.colNames = ['titulo', 'periodo', 'sesion', 'votacion', 'fecha', 'hora', 'total', 'presente', 'ausente', 'si', 'no', 'blanco', 'abstencion', 'asunto']
    self.sesDf = pd.DataFrame(columns=self.colNames)

  def validate_dir(self,path):
    if not os.path.exists(path):
      os.makedirs(path)

  def get_datasets(self):
    for folderName, subfolders, filenames in os.walk(self.pdfsfolder):
      for folder in subfolders:
        self.currentAge = folder[-4:]
        path = os.path.join(folderName, folder)
        for foldern2, subf2, fnames2 in os.walk(path):
          for folder2 in subf2:
            if self.currentAge == '2013' or self.currentAge == '2014':
              self.currentMonth = folder2
            else:
              self.currentMonth = folder2[:-4]
            path2 = os.path.join(foldern2, folder2)
            for foldern3, subf3, fnames3 in os.walk(path2):
              for folder3 in subf3:
                path3 = os.path.join(foldern3, folder3)
                for folder4, subf4, filenames4 in os.walk(path3):
                  count = 0
                  for files in filenames4:
                    path4 = os.path.join(folder4, files)
                    logging.info('Anio: ' + self.currentAge)
                    logging.info('Mes: ' + folder2)
                    logging.info('Sesion: ' + folder3)
                    logging.info('Nombre: ' + files)
                    logging.info('Pdf: ' + path4)
                    logging.info('')
                    print(path4)
                    self.csv.pdfdir = path4
                    try:
                      info = self.csv.get_info(count, self.currentAge, self.currentMonth)
                      name = self.csv.sesionName
                      verPath = self.basedir + name + '.csv'
                      if os.path.exists(verPath):
                        logging.info('Ya existe: ' + name)
                        self.sesDf = self.sesDf.append(pd.Series(info, index=self.colNames), ignore_index=True)
                        self.get_sesiones_csv() 
                      else:
                        dfs = self.csv.get_dfs()
                        dfconcat = self.csv.concat_dfs(dfs)
                        self.csv.get_csv(dfconcat, name)
                        self.sesDf = self.sesDf.append(pd.Series(info, index=self.colNames), ignore_index=True)
                        self.get_sesiones_csv()
                      logging.info('_______________')
                      logging.info('')
                    except Exception as e:
                      print(e)
                      print(self.sesDf)
                      self.get_sesiones_csv()
                      logging.warning('Error con el pdf: ' + files)
                      raise e
                    count += 1

  def get_sesiones_csv(self):
    path = self.indiceName
    self.sesDf.to_csv(path, index=False)

if __name__ == '__main__':
    logging.basicConfig(filename='logs/datasets_log.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')
    logger = logging.getLogger('__BDataset__')
    logging.info('------------------------------------------------------------------------------------------')
    logging.info('')
    logging.info('')
    logging.info('Starting')

    client = BDataset()
    client.validate_dir(client.basedir)
    client.get_datasets()