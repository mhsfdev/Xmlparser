import xml.etree.ElementTree as ET
from urllib.request import urlopen 
from datetime import datetime

from utils import log, read_file, write_to_file, compare_pulls, print_dict


xmlfeed_produkty = urlopen('https://www.jozanek.cz/Services/Feed.ashx?type=heureka.cz&key=uiroTARO68bl')
xmlfeed_stock = urlopen('https://www.jozanek.cz/Services/Feed.ashx?type=heureka.cz&key=uiroTARO68bl&avail=1')
    
mytree = ET.parse(xmlfeed_produkty)
myroot = mytree.getroot()

actual_pull = {}
error_log = {}
date = datetime.now().strftime("%Y_%m_%d-%I%M%S_%p")

diflog_name = 'difflog_'+date+'.txt'
errorlog_name = 'errorlog_'+date+'.txt'

actual_pull['product id']=(['EAN;name','price in CZK','# on stock']) # headeer
error_log['log date'] = [date]

"""
refactoring
 - vytvor separe funkciu na stiahnutie param(feed, list_of_keyowrds, output, name_of matching keyword)
 - ak nie je dany output dict, vrati novy, s list of keyword
 - nova trieda??
"""
#stiahni product list
for shopitem in myroot.findall('SHOPITEM'):
      
    available = True 
    if available : # writing only item on stock
        product_id = str(shopitem.find('ITEM_ID').text)
        
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
        product_id = str(item.attrib['id'])
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

previous_pull = read_file()
new_items,run_out_items = compare_pulls(previous_pull, actual_pull)
write_to_file(actual_pull,f'data_{date}.csv')
write_to_file(error_log,errorlog_name)

print ('new items :', len(new_items)-1)
print ('missing :', len(run_out_items)-1)
print ('details in :',diflog_name)

write_to_file({**run_out_items,**new_items}, diflog_name)





