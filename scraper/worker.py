import os, sys
import django
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mppp.settings')
django.setup()



import helper, linker, getter , merger, downer
import constants as C


started_time = datetime.now()

helper.printBanner()
helper.printMessage('===', 'worker', "========== The unlazy worker started working ==========", 1, 1)
helper.printMessage('===', 'worker', F"Arguments: VERBOSITY={C.VERBOSITY}, IMPORT_LINKS={C.IMPORT_LINKS}, REFRESH_EXISTING={C.REFRESH_EXISTING}", 0, 3)

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

helper.printMessage('===', 'worker', f"Saving data finished.", 1)

dceed, fceed = 0, 0
if C.SKIP_DCE:
    helper.printMessage('===', 'worker', "SKIP_DCE set. Skipping DCE files.")
else:
    i = 0
    helper.printMessage('INFO', 'worker', "Getting the list of DCE files to download ...", 1)
    dceables = downer.getFileables()
    c = dceables.count()
    helper.printMessage('INFO', 'worker', f"Started getting DCE files for { c } items ...")
    for d in dceables:
        i += 1
        helper.printMessage('INFO', 'worker', f"Getting DCE files for { i }/{ c } : { d.chrono } ...", 1)
        getdce = downer.getDCE(d)
        if getdce == 0:
            dceed += 1
            helper.printMessage('INFO', 'worker', f"DCE download for { d.chrono } was successfull.", 1)
        else:
            fceed += 1
            helper.printMessage('WARN', 'worker', f"Something went wrong whith DCE download for { d.chrono }.", 1)

        hceed = dceed + fceed
        if hceed > 0:
            if hceed % C.BURST_LENGTH == 0:
                helper.printMessage('INFO', 'worker', "Sleeping for a while.", 1)
                helper.sleepRandom(10, 30)
    helper.printMessage('INFO', 'worker', f"Downloaded DCE files for {dceed} items")
    helper.printMessage('INFO', 'worker', f"Failed to downloaded DCE files for {fceed} items")


finished_time = datetime.now()
it_took = finished_time - started_time

helper.printMessage('===', 'worker', f"Created {created}, updated {updated} Tenders. Downloaded {dceed} DCE files, {fceed} downloads failed.", 2)
helper.printMessage('===', 'worker', f"That took our unlazy worker { it_took }.")
helper.printMessage('===', 'worker', f"============ The unlazy worker is done working ============", 1, 1)
