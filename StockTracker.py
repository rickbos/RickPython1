import pandas as pd
import numpy as np
import yfinance as yf
import json
import json2html

def readCurrent(f1) : 

  print(f1)
  xls = pd.ExcelFile(f1)
  df1 = pd.read_excel(xls, 'QuestTrade')
  marginMap = {}
  priceMap = {}
  rrspMap = {}
  tfsaMap = {}
  cashMap = {}
  for i in range(2,20) : 
    name = df1.iloc[i][14]
    price = getNumber(df1.iloc[i][15])
    rrsp = getNumber(df1.iloc[i][16])
    tfsa = getNumber(df1.iloc[i][18])
    margin =getNumber( df1.iloc[i][20])
    totalUnits = rrsp + tfsa + margin
    rrspValue = price*rrsp
    tfsaValue = price*tfsa
    marginValue = price*margin
    value = totalUnits * price
    if ( name == 'Cash'):
        rrspValue = getNumber(df1.iloc[i][17])
        tfsaValue = getNumber(df1.iloc[i][19])
        marginValue = getNumber(df1.iloc[i][21])
        cashMap = {'rrsp' : rrspValue, 'tfsa': tfsaValue, 'margin' : marginValue}
    else: 
        if ( price > 0 ) :
          priceMap[name] =price
        if ( rrsp > 0 ) :
          rrspMap[name] = rrsp
        if ( tfsa > 0 ) :
          tfsaMap[name] = tfsa   
        if ( margin > 0 ) :
          marginMap[name] = margin    
  finalMap = {'cash': cashMap, 'prices': priceMap, 'rrsp': rrspMap, 'tfsa': tfsaMap, 'margin': marginMap}
  readDrip(xls,finalMap)
  readCoop(xls,finalMap)
  readPension(xls,finalMap)
  return finalMap

def saveMap( fname, finalMap):

  finalMap = {'investments':finalMap}

  with open(fname, 'w') as file:
     file.write(json.dumps(finalMap, indent =4) )  
  print('saved ' + fname)

def loadMap( fname):

  with open(fname) as user_file:
    file_contents = user_file.read()
    print(file_contents)
    parsed_json = json.loads(file_contents)
    return parsed_json
  
def readDrip(xls, finalMap) :
    df1 = pd.read_excel(xls, 'drip')
    units =  getNumber(df1.iloc[14][3])
    price = getNumber(df1.iloc[14][4])
    finalMap['prices']['BMO.TO'] = price
    finalMap['margin']['BMO.TO'] = units
    print('drip:' + str(units) + ' ' + str(price)+ ' ' +str(price*units))

def readCoop(xls, finalMap) :
    df1 = pd.read_excel(xls, 'CoopShares')
    units =  getNumber(df1.iloc[8][1])
    price = 100.0
    finalMap['prices']['CoopShares'] = price
    finalMap['margin']['CoopShares'] = units
    
    print('Coop:' + str(units) + ' ' + str(price)+ ' ' +str(price*units))

def readPension(xls, finalMap) :
    df1 = pd.read_excel(xls, 'Net')
    value =  getNumber(df1.iloc[6][23])
  
    finalMap['pension'] = value
  
    
    print('Coop Pension ' + str(value))

def displayMap( map1, priceKey):
   total = 0.0
   total = total + getTotal(map1[ priceKey], map1, 'rrsp')
   total = total + getTotal(map1[ priceKey], map1,'tfsa')
   total = total + getTotal(map1[ priceKey], map1,'margin')
   total = total + map1['pension']
   print(str(total))

def getCurrentPrices(prices) :
   current = {}
   for key in prices.keys():
      price = getCurrentPrice(key)
      print(key+":"+str(price))
      if ( price > 0.0):
        current[key] =  price
      else:
        current[key] = prices[key]
   for key in prices.keys():
      if ( abs( prices[key] - current[key]) > 1) : 
         print('Price changed: ' + key + ' ' + str(prices[key]) +  ' ' + str(current[key]))
   return current   

def getCurrentPrice(key):
   price = 0.0
   if ( not key.endswith('TO')):
         price = getCurrentPriceInternal(key+'.TO')
   else:
       price = getCurrentPriceInternal(key)
   if ( price == 0.0):
      price = getCurrentPriceInternal(key)
   return price

def getCurrentPriceInternal(key) :
  price = 0.0
  try:

    tick = yf.Ticker(key)
    data = tick.history()
    data = tick.history()
    last_quote = data['Close'].iloc[-1]  
    price = last_quote
  except: 
     price =0.0 
  return price
def getTotal(prices, mapAll, account) :
   total = 0.0
   map1 = mapAll[account]
   for key in map1.keys():  
      total = total + map1[key]*prices[key]
   total = total + mapAll['cash'][account]
   return total   

def getNumber ( n ) :
  x = 0 
  try:
    if np.isnan(n):
       x = 0
    else:
      if isinstance(n, (int, float, complex)):  
        x = n
  except:
      x = 0 
  return x 

def saveHTML( jFile, hFile):
 print(hFile)
 with open(jFile) as user_file:
    file_contents = user_file.read()
    infoFromJson =json.loads(file_contents)
    html=json2html.json2html.convert(json = infoFromJson)
    with open(hFile, 'w') as file:
     file.write(html) 
     print('saved : ' + hFile)

def main():
  dataDir = 'E:\\data\\important\\finances\\data\\'
  excelFile = dataDir + 'net.ods'
  jsonFile = dataDir + 'invest.json'
  htmlFile = dataDir + 'invest.html'
  #current = readCurrent(  excelFile)
  current = loadMap(jsonFile)['investments']
  #current['latestPrices'] = getCurrentPrices(current['prices'])
  displayMap(current, 'prices')
  displayMap(current, 'latestPrices')
  saveHTML( jsonFile,htmlFile)
 # saveMap(jsonFile, current)
  #map2 = loadMap(jsonFile)
  #print(map2)
  #displayMap(map2['investments'],'prices')
if __name__ == "__main__":

   main()
