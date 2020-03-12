from requests import get
from urllib.parse import urljoin
import os
from os import path, getcwd, makedirs
from bs4 import BeautifulSoup as soup
import sys
import logging


class PdfClient:
  '''
  Cliente para obtener las sessiones de la asamblea en los años 2013 - 2020 en adelante
  '''
  def __init__(self):
    self.base_url = 'http://guest:guest@documentacion.asambleanacional.gob.ec'
    self.url = 'http://guest:guest@documentacion.asambleanacional.gob.ec/alfresco/webdav/Documentos%20Web/Votaciones%20del%20Pleno'
    self.base_dir = 'pdfs/'
    self.current_dir = ''
    self.mesdir = ''
    self.tmpdir = ''

  def get_page(self, base_url):
    req = get(base_url)
    if req.status_code == 200:
        return req.text
    logging.warning('http status_code: ' + req.status_code)
    raise Exception('Error {0}'.format(req.status_code))

  def get_all_links(self, html):
    bs = soup(html, 'html.parser')  # MISSING 'html.parser'
    #print(bs.prettify())
    links = bs.findAll('a')
    links = links[1:]
    return links

  def get_links_to_nav(self, base_url):
    html = self.get_page(base_url)  # MISSING ARGUMENT
    links = self.get_all_links(html)

    if len(links) == 0:
      logging.warning('No links found on the webpage.')
      #raise Exception('No links found on the webpage')
    return links

  def validate_name(self, text):
    tmp = ''
    size = len(text)
    if (len(text) > 120):
      tmp = text[:110]
      tmp2 = tmp[-4:]
      #print(tmp2)
      #print(tmp)
      if (tmp2 != '.pdf'):
        tmp = tmp + '.pdf'    
      return tmp
    return text

  def validate_dir(self,path):
    if not os.path.exists(path):
      makedirs(path)

  def get_pdf(self, base_url, base_dir):

    logging.info(' ')
    logging.info(' ')
    logging.info('---------------------------')
    html = self.get_page(base_url)  # MISSING ARGUMENT
    links = self.get_all_links(html)
    if len(links) == 0:
        logging.warning('No links found on the webpage.')
        #raise Exception('No links found on the webpage')

    n_pdfs = 0
    n_saved_pdfs = 0
    logging.info('Pdfs Total: ' + str(len(links)))

    for link in links:
        
        current_link = link.get('href')  # This line and the line below
        text = link.contents
        name = self.validate_name(text[0])
        logging.info('Info pdf: ' + str(text))
        logging.info('Nombre pdf: ' + str(name))

        if current_link.endswith('pdf'):
            weblink = urljoin(base_url, link['href'])
            logging.info('pdf file found at ' + str(weblink))
            #print('pdf file found:', weblink)

            n_pdfs += 1

            file_address = path.join(base_dir, name)

            if path.exists(file_address) == False:
                content = get(weblink, stream=True)  # https://stackoverflow.com/a/44299915/2449724
                # stream=True means when function returns, only the response header is downloaded, response body is not.

                if content.status_code == 200 and content.headers[
                    'content-type'] == 'application/pdf':  # status to status_code
                    value = round(float(content.headers['Content-length']) / 1000000, 2)
                    logging.info('File size(mb): ' + str(value) )
                    with open(file_address, 'wb') as pdf:
                        logging.info('Saving pdf to ' + file_address)
                        #print('Saving pdf to', file_address)

                        pdf.write(content.content)

                        logging.info('COMPLETE')
                        #print('COMPLETE')

                        n_saved_pdfs += 1
                        logging.info('Number of save pdfs is ' + str(n_saved_pdfs))
                        #print()
                else:
                    logging.info('content.status_code: ' + str(content.status_code))
                    logging.info('''content.headers['content-type']:''' + content.headers['content-type'])
                    #print('content.status_code:', content.status_code)
                    #print('''content.headers['content-type']:''', content.headers['content-type'])
                    #print()

            else:
                logging.info('Already saved.!')
                #print('Already saved')
                n_saved_pdfs += 1
                #print()
        if n_pdfs == 0:
            logging.warning('No pdfs found on the page.')

        logging.info("{0} pdfs found, {1} saved in {2}".format(n_pdfs, n_saved_pdfs, base_dir))
        #print("{0} pdfs found, {1} saved in {2}".format(n_pdfs, n_saved_pdfs, base_dir))
        logging.info('_________________________ !')
        logging.info(' ')
        

  def get_all_sessions(self, base_url, url, base_dir):
    links = self.get_links_to_nav(url)
    for link in links:
      #Anios 2013-2018
      current_link = link.get('href')
      
      text = link.contents
      name = self.validate_name(text[0])
      current_dir = base_dir + name + '/'
      self.validate_dir(current_dir)
      
      current_link = base_url + current_link
      meses = self.get_links_to_nav(current_link)
      #meses = meses[1:]
      for mes in meses:
        #Meses del año correspondiente
        current_mes = mes.get('href')

        textM = mes.contents
        name = self.validate_name(textM[0])
        
        mesdir = current_dir + name + '/'
        self.validate_dir(mesdir) 

        current_mes = base_url + current_mes
        sesiones = self.get_links_to_nav(current_mes)
        #sesiones = sesiones[1:]
        for sesion in sesiones:
          #sesion actual 
          sesion_link = sesion.get('href')

          text = sesion.contents
          name = self.validate_name(text[0])
          tmpdir = mesdir + name + '/'
          #current_dir = current_dir + name + '/'
          self.validate_dir(tmpdir)

          sesion_link = base_url + sesion_link
          logging.info('              #SESION                        ')
          logging.info(' --------- ' + name + ' --------------------')
          self.get_pdf(sesion_link, tmpdir)

if __name__ == '__main__':
  client = PdfClient()
  basedir = client.base_dir
  baseurl = client.base_url
  url = client.url
  logging.basicConfig(filename='logs/pdfs_log.log' , filemode='w', level=logging.INFO, format='%(asctime)s %(message)s')
  logger = logging.getLogger('__FileServer__')
  logging.info('------------------------------------------------------------------------------------------')
  logging.info('')
  logging.info('')
  logging.info('Starting')
  logging.info('base_url: ' + baseurl)
  logging.info('base_dir: ' + basedir)

  client.get_all_sessions(baseurl, url, basedir)