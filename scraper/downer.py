
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

import os
from datetime import datetime, timedelta

import helper
import constants as C

from scraper.models import Tender, Change

def getFileables(past_days=C.CLEAN_DCE_AFTER_DAYS):

    fresh_tenders = Tender.objects.filter(files_to_get__closed=False).distinct()
    nodce_tenders = get_tenders_without_files()

    return fresh_tenders | nodce_tenders


def get_tenders_without_files(batch_size=1000):

    target_date = datetime.now() - timedelta(days=past_days)
    current_tenders = Tender.objects.filter(deadline__gte=target_date)

    tenders_without_files = []
    for tender_id, chrono in current_tenders.values_list('id', 'chrono').iterator(chunk_size=batch_size):
        if chrono:
            if is_empty_or_nonexistent(f"{C.MEDIA_ROOT}/dce/{DL_PATH_PREFIX}{chrono}"):
                tenders_without_files.append(tender_id)

    return current_tenders.filter(id__in=tenders_without_files)

def is_empty_or_nonexistent(folder_path):
    if not os.path.exists(folder_path):
        return True
    return not any(os.path.isfile(os.path.join(folder_path, item)) for item in os.listdir(folder_path))