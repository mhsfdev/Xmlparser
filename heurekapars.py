import xml.etree.ElementTree as ET
from urllib.request import urlopen 
from time import asctime
import csv

def print_dict(dicto,n=30):
    counter = 0
    for key, value in dicto.items():
        line = str(key)+';'
        line += ';'.join(value)
        
        print(line)
        counter +=1
        if counter == n:break

def write_to_file(data, filename):
    if type(data) != dict:
        raise TypeError
    
    try :
        f = open(file=filename, mode='wt')
        for key, value in data.items():
            line = str(key)+';'
            line += ';'.join(value)
            
            print(line, file = f)
        

    finally:
        
        f.close()

def read_file(): # reads last feed log into dictionary
    
    dicto = {}
    feed = open(file='data.csv', mode ='r', encoding = 'utf-8')
    csv_reader = csv.reader(feed)
    

    for row in csv_reader:
        key = row[0]
        value = [x for x in row[1:] ]
        dicto[key] = value
    feed.close()
    return dicto

    
def log(logdict,item_id, text):
    if item_id not in logdict.keys():
        logdict[item_id] = [text]
        return
    else:
        item_to_update = logdict.get(item_id)
        item_to_update.append(text)
        
        logdict[item_id] = item_to_update
        return
    

 # data file 


xmlfeed_produkty = urlopen('https://www.jozanek.cz/Services/Feed.ashx?type=heureka.cz&key=uiroTARO68bl')
xmlfeed_stock = urlopen('https://www.jozanek.cz/Services/Feed.ashx?type=heureka.cz&key=uiroTARO68bl&avail=1')
    
mytree = ET.parse(xmlfeed_produkty)
myroot = mytree.getroot()

actual_pull = {}
error_log = {}
print_dict(read_file())

actual_pull['product id']=(['EAN;name','price in CZK','# on stock']) # headeer
error_log['log date'] = [asctime()]

#stiahni product list
for shopitem in myroot.findall('SHOPITEM'):
      
    available = True 
    if available : # writing only item on stock
        product_id = shopitem.find('ITEM_ID').text
        
        if shopitem.find('EAN') != None:

            ean = shopitem.find('EAN').text 
        else :
            ean = 'None'
            log(error_log, product_id, 'missing EAN')
        
        name = shopitem.find('PRODUCTNAME').text
        price = shopitem.find('PRICE_VAT').text
        #picture = item.find('g:image_link').text
        
            
        actual_pull[product_id]=[ean, name, price]
print ('items processed', len(actual_pull)) 

# stiahni stav skladu
mytree = ET.parse(xmlfeed_stock)
myroot = mytree.getroot()

for item in myroot.findall('item'):
    if item.attrib['id'] != None:
        product_id = item.attrib['id']
        if item.find('stock_quantity') != None:
            pcs_on_stock = item.find('stock_quantity').text  
        else:
            log(error_log, product_id, 'missing pcs on stock')
            continue
        if product_id in actual_pull.keys():

            item_to_update = actual_pull.get(product_id)  
        else :
            log(error_log, product_id, 'not in product feed')
            continue
    item_to_update.append(pcs_on_stock)
    actual_pull[product_id] = item_to_update 

write_to_file(actual_pull,'data.csv')
write_to_file(error_log,'errorlog.txt')




