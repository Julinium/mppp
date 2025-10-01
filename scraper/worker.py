import os, sys
import django

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mppp.settings')
django.setup()



import json

import helper, linker, getter , merger, downer
import constants as C


# IMPORT_LINKS = C.IMPORT_LINKS
# REFRESH_EXISTING = C.REFRESH_EXISTING

# REFRESH_EXISTING = True
# IMPORT_LINKS = True

helper.printBanner()
helper.printMessage('INFO', 'worker', "========== The unlazy worker started working ==========", 1, 1)
helper.printMessage('INFO', 'worker', F"Arguments: VERBOSITY={C.VERBOSITY}, IMPORT_LINKS={C.IMPORT_LINKS}, REFRESH_EXISTING={C.REFRESH_EXISTING}", 0, 3)

links = []
if not C.IMPORT_LINKS:
    links = linker.getLinks()
    linker.exportLinks(links)
else:
    links = helper.importLinks()

ll = len(links)
helper.printMessage('DEBUG', 'worker', f"Count of links to handle: {ll} ...", 1)

created, updated = 0 , 0
if ll > 0:
    i = 0
    helper.printMessage('INFO', 'worker', f"Getting Data for {ll} links ... ", 1)
    links =  reversed(links) # Browse links in reverse order.
    for l in links:
        handled = created + updated
        i += 1
        helper.printMessage('INFO', 'worker', f"Getting Data for link {i:03}/{ll:03}", 2)
        jsono = getter.getJson(l, not C.REFRESH_EXISTING)
        if jsono:
            tender, creation_mode = merger.save(jsono)
            if creation_mode == True: 
                created += 1
                helper.printMessage('INFO', 'worker', f"Created Tender {tender.chrono}")
            elif creation_mode == False: 
                updated += 1
                helper.printMessage('INFO', 'worker', f"Updated Tender {tender.chrono}")

        
        if handled > 0:
            if handled % C.BURST_LENGTH == 0:
                helper.printMessage('INFO', 'worker', "Sleeping for a while.", 1)
                helper.sleepRandom(10, 30)
else:
    helper.printMessage('ERROR', 'worker', "========== Links list was empty ==========", 2, 3)

helper.printMessage('INFO', 'worker', f"Saving data finished. Created {created}, updated {updated} Tenders.", 2, 1)

if C.SKIP_DCE:
    helper.printMessage('INFO', 'worker', "SKIP_DCE set. Skipping DCE files.")
else:
    i, dceed = 0, 0
    helper.printMessage('INFO', 'worker', "Getting the list of DCE files to download ...", 2, 1)
    dceables = downer.getFileables()
    c = dceables.count()
    helper.printMessage('INFO', 'worker', f"Started getting DCE files for { c } items ...")
    for d in dceables:
        i += 1
        helper.printMessage('INFO', 'worker', f"Getting DCE files for item { d.chrono }: { i }/{ c } ...", 2)
        if downer.getDCE(d) == 0:
            dceed += 1
        if dceed > 0:
            if dceed % C.BURST_LENGTH == 0:
                helper.printMessage('INFO', 'worker', "Sleeping for a while.", 1)
                helper.sleepRandom(10, 30)
    helper.printMessage('INFO', 'worker', f"Downloaded DCE files for {dceed} items", 2)

helper.printMessage('INFO', 'worker', f"====================== Done ======================", 3, 1)
