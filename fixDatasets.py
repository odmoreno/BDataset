import csv
import sys
import pandas as pd
import os

#sys.setdefaultencoding('utf-8')
'''
basefolder ='cvnetworks/periodo1/'
name = 'cv_sesion_0_p1_a2013_m05_v1.csv' 
path = name
cols = ['A1', 'A2', 'valor']
df = pd.DataFrame([], columns=cols)
ignorefirst = True

with open(path, 'r' ,encoding="latin-1" , newline='') as file:
    rd = csv.reader(file)
    
    for row in rd: 
      #print(row)
      if not ignorefirst:
        df = df.append(pd.Series(row, index=cols), ignore_index=True)
        df.to_csv('out.csv', index=False)
      else:
        ignorefirst=False 
    print('fin')
         
'''

#in_path = name
#out_path = 'Out.csv'
#
#with open(name, 'r', encoding="latin-1", newline='') as inputFile, open(out_path, 'w', newline='') as writerFile:
#    read_file = csv.reader(inputFile)
#    write_file = csv.writer(writerFile)
#
#    for row in read_file:
#      #list = [row[0].encode("utf-8"), row[1].encode("utf-8"), row[2]]
#      #print(list)
#      #row = list
#      print(row)
#      write_file.writerow(row)

class Fix:

  def __init__(self):
    self.basefolder = '_periodo1/'
    self.foldertosave = 'periodo1_fix/'
    self.ignorefirst = True
    self.cols = ['A1', 'A2', 'valor']

  def loop(self):
    for folderName, subfolders, filenames in os.walk(self.basefolder):
      for files in filenames:
        self.ignorefirst = True
        df = pd.DataFrame([], columns=self.cols)
        print(files)
        path = self.basefolder + files
        with open(path, 'r' , encoding='ISO-8859-1' , newline='') as file:
          rd = csv.reader(file)
          for row in rd:
            if not self.ignorefirst:
                #print(row)
                #list = [unicode(cell, 'utf-8') for cell in row]
                df = df.append(pd.Series(row, index=self.cols), ignore_index=True)
                newpath = self.foldertosave + files
                df.to_csv(newpath, index=False)
            else:
              self.ignorefirst=False 
          print('------ Fix :' + files)

if __name__ == "__main__":
  client = Fix()
  client.loop()    