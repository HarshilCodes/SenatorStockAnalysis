import csv, json, zipfile
import requests
import PyPDF2
import fitz
import re 
import yfinance as yf
 
class StockHolding: 
       def __init__(self):
           self.List = []
    #  def __init__(self,name,status,state):
    #      self.name = name
    #      self.status = status
    #      self.state = state
    
       def addToList(self, security):
           self.List.append(security)
        
       def getList(self):
           return self.List 
          

         
class Security: 
     def __init__(self,asset):
         self.asset = asset

     def getAsset(self):
         return self.asset


url_name = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2021FD.ZIP'
stockholding_file_url = 'https://www.snopes.com/uploads/2021/02/'
req = requests.get(url_name)
 
file_name = "finances.zip"
with open(file_name, 'wb') as f: 
    f.write(req.content)

with zipfile.ZipFile(file_name) as z: 
    z.extractall('.')

# with open('20018011.pdf', 'rb') as l:
#     reader = PyPDF2.PdfFileReader(l)
#     page1 = reader.getPage(1)
#     # getText = page1.extractText()
#     # print(getText)


with open('2021FD.txt') as l:
     for line in csv.reader(l, delimiter ='\t'):
        if line[1] == 'Pelosi':
            print(line)
            date = line[7]
            doc_id = line[8]

            req = requests.get(f"{stockholding_file_url}{doc_id}.pdf")

            with open(f"{doc_id}.pdf",'wb') as r1: 
                r1.write(req.content)

doc = fitz.open('20018011.pdf')
page = doc.load_page(page_id =0)
print(page.get_text())
sH = StockHolding() 
for word in page.get_text("words"):
    if(word[4][0:1] == '('): 
        #  print(word[4])
         s = Security(word[4])
         sH.addToList(s)

copyList = sH.getList()

for obj in copyList: 
    print(obj.getAsset()[1:len(obj.getAsset()) -1])
    tick = yf.Ticker(obj.getAsset()[1:len(obj.getAsset()) -1])
    # print(tick.dividends)
    tickerDF = tick.history(period='1d', start='2010-1-1', end='2020-1-25')
    print(tickerDF)

             




