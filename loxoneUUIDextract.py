import json, urllib, urllib.request, sys

def clean_names(uncleared):
    return uncleared.replace(" ","_")

#debug variables
printrooms = False
printcats = False
printall = False
###############################################



# Import System Config file. Same syntax
# read and parse file 
with open('system_config.json', 'r') as importedConfig:
    importedData=json.loads(importedConfig.read())

#copy config to export dataset
dataexport = importedData
dataexport['uuids'] = {}

#read from file or fetch via http from miniserver
readmode = 0

if (readmode > 0):
    # read file
    with open('loxone3.json', 'r') as myfile:
        data=myfile.read()
        # parse file
        lox = json.loads(data)
else:
    miniserver = importedData['loxone']['host']
    username = importedData['loxone']['username']
    password = importedData['loxone']['password']
    
    top_level_url = "http://" + miniserver 
    url = top_level_url + "/data/LoxAPP3.json"

    # password manager
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, top_level_url, username, password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)

    # fetch 
    response = opener.open(url)
    print("HTTP Status " + str(response.status))
    if response.status > 299:
        sys.exit()

    #parse to json
    lox = json.loads(response.read())


if printrooms:
    for item in lox['rooms']:
        print("Raum ",lox['rooms'][item]['name'],"  ID: ",lox['rooms'][item]['uuid'])

if printcats:
    for item in lox['cats']:
        print("categorie ",lox['cats'][item]['name'],"  ID: ",lox['cats'][item]['uuid'])


for item in lox['controls']:
    roomid = lox['controls'][item]['room']
    roomstring = clean_names(lox['rooms'][roomid]['name'])
    namestring = clean_names(lox['controls'][item]['name'])
    
    
    catid =  lox['controls'][item]['cat']
    catstring = clean_names(lox['cats'][catid]['name'])

    
    uuid = ' '
    outputcounter = 0
    if "statistic" in lox['controls'][item]:
        for output in lox['controls'][item]['statistic']['outputs']:
            outputstring = clean_names(output['name'])
            outputcounter = outputcounter + 1

        for output in lox['controls'][item]['statistic']['outputs']:
            outputstring = clean_names(output['name'])
            uuid = output['uuid']
            
            if outputcounter > 1:
                if printall:
                    print(roomstring,catstring,namestring,outputstring) 
                dataset = {uuid:{"measurement":namestring , "tags": {"room":roomstring, "output":outputstring}, "intervalSec":0}}
            else:
                if printall:
                    print(roomstring,catstring,namestring)
                dataset = {uuid:{"measurement":namestring , "tags": {"room":roomstring }, "intervalSec":0}}
            dataexport['uuids'].update(dataset)
        for state in lox['controls'][item]['states']:
            if state == 'value' or state == 'active' or state == 'tempActual' or state == 'tempTarget' or state == 'actual' or state == 'total':
                uuid = lox['controls'][item]['states'][state]
                dataset = {uuid:{"measurement":namestring + "-" + state , "tags": {"room":roomstring }, "intervalSec":0}}
                dataexport['uuids'].update(dataset)
            else:
                if printall:
                    print(state)
        

    
with open("local.json", "w") as write_file:
    json.dump(dataexport, write_file, indent=2)


print("Done")

