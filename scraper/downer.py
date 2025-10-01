
# 01. Make a list of items to handle:
    ## Items with deadline later than a given date (past N days).
    ## Special items (failed previously, requested, ...)

# 02. Loop over the "list" of items:
    ## If refresh is required, delete files if any.
    ## If no files, get the files.
    ## If item in a special list, remove it.


# 03. Periodically, check for and delete:
    ## Orphan files.
    ## Files for items over certain age old.


import helper
import constants as C

from scraper.models import Tender, Change

def getFileables():
    tenders = Tender.objects.filter(files_to_get__closed=False).distinct()

    return tenders