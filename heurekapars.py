import xml.etree.ElementTree as ET
from urllib.request import urlopen 

def print_dict(dicto,n=10):
    counter = 0
    for key, value in dicto.items():
        line = str(key)+';'
        line += ';'.join(value)
        
        print(line)
        counter +=1
        if counter == n:break

 # data file 
"""
  vytvorit logovacie subory / chyby - chybaj[ce id, ean , stavy
  ]
"""

xmlfeed_produkty = urlopen('https://www.jozanek.cz/Services/Feed.ashx?type=heureka.cz&key=uiroTARO68bl')
xmlfeed_stock = urlopen('https://www.jozanek.cz/Services/Feed.ashx?type=heureka.cz&key=uiroTARO68bl&avail=1')
    
mytree = ET.parse(xmlfeed_produkty)
myroot = mytree.getroot()

product_list = {}

product_list['product id']=(['EAN;name','price in CZK','# on stock']) # headeer

#stiahni product list
for shopitem in myroot.findall('SHOPITEM'):
        
    available = True 
    if available : # writing only item on stock
        product_id = shopitem.find('ITEM_ID').text
        
        ean = shopitem.find('EAN').text if shopitem.find('EAN') != None else 'None'
        
        name = shopitem.find('PRODUCTNAME').text
        price = shopitem.find('PRICE_VAT').text
        #picture = item.find('g:image_link').text
        
            
        product_list[product_id]=[ean, name, price]
        

# stiahni stav skladu
mytree = ET.parse(xmlfeed_stock)
myroot = mytree.getroot()

for item in myroot.findall('item'):
    product_id = item.attrib['id']
    if item.find('stock_quantity') != None:
        pcs_on_stock = item.find('stock_quantity').text  
    else:
        continue
    if product_list.get(product_id) != None:

        item_to_update = product_list.get(product_id)  
    else :
        print(f'product with id{product_id} is not in product feed')
        continue
    item_to_update.append(pcs_on_stock)
    product_list[product_id] = item_to_update 

try :
    csv = open(file='datatest.csv', mode='w')
    for key, value in product_list.items():
        line = str(key)+';'
        line += ';'.join(value)
        
        print(line, file = csv)
        

finally:
    csv.close()

print_dict(product_list)
