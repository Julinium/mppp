
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

def tenders2download():
    tenders = Tender.objects.all()

    return tenders

    python manage.py makemigrations myapp
    usage: manage.py [-h] [--arg1 ARG1] [--arg2 ARG2] [--arg3 ARG]
    manage.py: error: unrecognized arguments: makemigrations myapp