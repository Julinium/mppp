import json

from . import helper, linker, getter , merger
from . import constants as C


IMPORT_LINKS = C.IMPORT_LINKS
REFRESH_EXISTING = C.REFRESH_EXISTING

REFRESH_EXISTING = True
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

    for l in links[::-1]:
        i += 1
        helper.printMessage('DEBUG', 'worker', f"Getting Data for link {i:03}/{ll:03}", 2, 1)
        jsono = getter.getJson(l, not REFRESH_EXISTING)
        if jsono:
            merger.saveTender(jsono)
    
helper.printMessage('INFO', 'worker', f"====================== Done ======================", 3, 1)
