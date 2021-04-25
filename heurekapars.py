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
  prerobit parserA na feedy heureka, aby sa zabezpecila kompatibilita
"""

xmlfeed_produkty = urlopen('https://www.jozanek.cz/Services/Feed.ashx?type=googleNakupy.cz&key=uiroTARO68bl')
xmlfeed_stock = urlopen('https://www.jozanek.cz/Services/Feed.ashx?type=heureka.cz&key=uiroTARO68bl&avail=1')
    
mytree = ET.parse(xmlfeed_produkty)
myroot = mytree.getroot()

product_list = {}
ns = {'BEG':"http://base.google.com/ns/1.0"} # namespace of the feed
product_list['product id']=(['EAN;name','price in CZK','# on stock']) # headeer

#stiahni product list
for item in myroot[0].findall('item'):
        
    available = True if item.find('BEG:availability',ns).text == 'in stock' else False
    if available : # writing only item on stock
        product_id = item.find('BEG:id', ns).text
        
        ean = item.find('BEG:gtin',ns).text if item.find('BEG:gtin',ns) != None else 'None'
        
        name = item.find('title').text
        price = item.find('BEG:price',ns).text
        #picture = item.find('g:image_link').text
        stock = item.find('BEG:availability',ns).text
            
        product_list[product_id]=[ean, name, price]

# stiahni stav skladu
mytree = ET.parse(xmlfeed_stock)
myroot = mytree.getroot()

for item in myroot.findall('item'):
    product_id = item.attrib['id']
    pcs_on_stock = item.find('stock_quantity').text
    new_item = product_list[product_id]
    new_item.append(150)
    product_list[product_id]=new_item

try :
    csv = open(file='datatest.csv', mode='w')
    for key, value in product_list.items():
        line = str(key)+';'
        line += ';'.join(value)
        
        print(line, file = csv)
        

finally:
    csv.close()

print_dict(product_list)
