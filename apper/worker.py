import json

import helper, linker, getter, merger
import constants as C


IMPORT_LINKS = C.IMPORT_LINKS
IMPORT_LINKS = True

# helper.printBanner()
helper.printMessage('INFO', 'worker', "========== The unlazy worker started working ==========", 1, 2)

links = []
if not IMPORT_LINKS:
    links = linker.getLinks()
    linker.exportLinks(links)
else:
    links = helper.importLinks()

if len(links) < 1:
    helper.printMessage('ERROR', 'worker', "========== Links list was empty ==========", 2, 2)


ll = len(links)
if ll > 0:
    file_path = "exports/cons.json"
    i = 0

    # with open(file_path, 'w') as file:
    #     pass

    # with open(file_path, 'a') as file:
    #     file.write('[\n')

    for l in links:
        i += 1
        helper.printMessage('DEBUG', 'worker', f"Getting JSON for link {i:03}/{ll:03}", 1, 0)
        jsono = getter.getJson(l)

        merger.mergeTender(jsono)
        
        # with open("exports/cons.json", 'a') as file:
        #     json.dump(jsono, file, indent=4)  # indent=4 for pretty-printed JSON
        #     file.write(',\n')
    
    # with open(file_path, 'a') as file:
    #     file.write('\n]')

