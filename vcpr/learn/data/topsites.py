from ... import constants
import requests, csv
from zipfile import ZipFile
from io import BytesIO, TextIOWrapper

URL = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
LIMIT = 20 ** 4

def download():
  with open(constants.TOPSITES, 'w') as f:
    with ZipFile(BytesIO(requests.get(URL, stream=True).content)) as zf:
      with zf.open(zf.namelist()[0]) as csvf:
        for x, site in csv.reader(TextIOWrapper(csvf)):
          if int(x) > LIMIT:
            break
          f.write(site + '\n')

if __name__ == '__main__':
  download()
