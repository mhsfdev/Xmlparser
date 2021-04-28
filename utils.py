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
        f = open(file=filename, mode='wt',encoding='utf-8')
        for key, value in data.items():
            line = str(key)+';'
            line += ';'.join(value)
            
            print(line, file = f)
        

    finally:
        
        f.close()

def read_file(): # reads last feed log into dictionary
    
    dicto = {}
    feed = open(file='data.csv', mode ='r', encoding = 'utf-8')
    csv_reader = csv.reader(feed, delimiter = ';' )
    

    for row in csv_reader:
        key = str(row[0])
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

def compare_pulls(previous, current):
    new_items={}
    new_items['new items as of:']= [asctime()]
    for key in current.keys():
        if str(key) not in previous:
            new_items[key] = current.get(key)

    missing_items={}
    missing_items['missing items as of :']=[asctime()]
    for key in previous.keys():
        if str(key) not in current:
            missing_items[key]=previous.get(key)
    
    return new_items, missing_items