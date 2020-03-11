import os
import pandas as pd
import logging

import csvClient

class BDataset:

  def __init__(self):
    self.pdfsfolder = 'pdfs/'
    self.csv = csvClient.ADataset()
    self.currentsession = ''
    self.indiceName = 'sesiones.csv'
    self.currentAge = ''
    self.colNames = ['titulo', 'periodo', 'sesion', 'votacion', 'fecha', 'hora', 'total', 'presente', 'ausente', 'si', 'no', 'blanco', 'abstencion', 'asunto']
    self.sesDf = pd.DataFrame(columns=self.colNames)

  def get_datasets(self):
    for folderName, subfolders, filenames in os.walk(self.pdfsfolder):
      for folder in subfolders:
        self.currentAge = folder[-4:]

        path = os.path.join(folderName, folder)
        for foldern2, subf2, fnames2 in os.walk(path):
          for folder2 in subf2:
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
                    logging.info('_______________')
                    logging.info('')
                    print(path4)
                    self.csv.pdfdir = path4
                    try:
                      dfs = self.csv.get_dfs()
                      dfconcat = self.csv.concat_dfs(dfs)
                      info = self.csv.get_info(count, self.currentAge)
                      name = self.csv.sesionName
                      self.csv.get_csv(dfconcat, name)
                      self.sesDf = self.sesDf.append(pd.Series(info, index=self.colNames), ignore_index=True)
                    except Exception as e:
                      print(e)
                      print(self.sesDf)
                      path = self.csv.basedir + self.indiceName
                      self.sesDf.to_csv(path, index=False)
                      logging.warning('Error con el pdf: ' + files)
                      raise e
                    count += 1

if __name__ == '__main__':
    logging.basicConfig(filename='datasets_log.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')
    logger = logging.getLogger('__BDataset__')
    logging.info('------------------------------------------------------------------------------------------')
    logging.info('')
    logging.info('')
    logging.info('Starting')

    client = BDataset()
    client.get_datasets()