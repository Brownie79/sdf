## Unzip SDF.zip into temp
## Load Cards into memory
## Replace the asset values with path for the unzipped files
## Run through with Mustache
## 
import os
import sys
from zipfile import ZipFile
import pystache
import yaml
import imgkit
import tempfile

def loadDeck(fileUrl):
  deckfile = ZipFile(fileUrl)
  #path = os.getcwd().replace('\\','/') + "/temp_dir/"
  path = tempfile.TemporaryDirectory().name.replace("\\", "/") + "/"
  
  deckfile.extractall(path)
  #deckyaml = yaml.load(open(path+'deck.yaml','r'), Loader=yaml.FullLoader)

  os.mkdir('deckimgs')
  for c in os.listdir(path+'/cards/'):
    card = yaml.load(open(path+"cards/"+c, 'r'), Loader=yaml.FullLoader)

    #Replace asset urls with path
    assetspath = 'file:///' + path + "assets/"
    #assetspath = "assets/"
    for asset in card['assets']:
      card['assets'][asset] = assetspath + card['assets'][asset]
    
    #sub the data and assets into the card
    
    templatepath = path+'templates/'+card['cardType']+'.svg'
    frontSVG = open(templatepath, 'r').read()
    cardSVG = pystache.render(frontSVG, card)
    
    outputPath = "deckimgs/"+c.replace(".yaml", "")+'.png'
    options = {'width': 600, 'height':450, 'disable-smart-width': ''}
    imgkit.from_string(cardSVG, outputPath, options=options)


if __name__ == "__main__":
  fileUrl = sys.argv[1]
  loadDeck(fileUrl)