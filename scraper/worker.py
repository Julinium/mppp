import helper, linker
import constants as C


# helper.printBanner()
helper.printMessage('INFO', 'worker', "========== The unlazy worker started working ==========", 1, 2)

links = []
if C.IMPORT_LINKS:
    links = linker.getLinks()
    linker.exportLinks(links)
else:
    links = helper.importLinks()

if len(links) < 1:
    helper.printMessage('ERROR', 'worker', "========== Links list was empty ==========", 2, 2)

