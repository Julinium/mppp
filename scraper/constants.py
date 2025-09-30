import os, argparse, json
from dotenv import load_dotenv
from pathlib import Path


SELENO_DIR = str(Path(__file__).resolve().parent)
env_path = f'{ SELENO_DIR }/.env'
load_dotenv(dotenv_path=env_path)


# More verbose output
# DEBUG_MODE = True 
VERBOSITY = 1
BURST_LENGTH = 25

LOGS_LEVELS = {
    "TRACE" : 1,
    "DEBUG" : 2,
    "INFO"  : 3,
    "WARN"  : 4,
    "ERROR" : 5,
    "FATAL" : 6,
}

# Instead of scraping the target website for items links, use those previously saved in imports/links.csv
IMPORT_LINKS = False

# Check existing items against portal for changes.
REFRESH_EXISTING = True

# Skip downloading DCE files.
SKIP_DCE = True


# Initialize parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('--level', type=str, required=False, help='debug for more verbose output.')
parser.add_argument('--links', type=str, required=False, help='import to use already saved links.')
parser.add_argument('--found', type=str, required=False, help='refresh to refresh existing items.')
parser.add_argument('--dce', type=str, required=False, help='DCE files download.')


# Parse arguments
args = parser.parse_args()
if args.level: 
    level = args.level.upper()
    if level in LOGS_LEVELS:
        VERBOSITY = LOGS_LEVELS[level]

if args.links: IMPORT_LINKS = args.links.lower() == "import"
if args.found: REFRESH_EXISTING = args.found.lower() == "refresh"
if args.dce: SKIP_DCE = args.dce.lower() != "download"


# Use Chromium without GUI. Set to True if running on a non-GUI system
HEADLESS_MODE = True #False

# Target website. Held for privacy
SITE_ROOT = os.getenv("SITE_ROOT")
SITE_INDEX = os.getenv("SITE_INDEX")
LINK_PREFIX = os.getenv("LINK_PREFIX")
LINK_STITCH = os.getenv("LINK_STITCH")

# Database credentials. Held for security
DB_SERVER = os.getenv("DB_SERVER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

ua_json = f'{ SELENO_DIR }/.env.ua.json'
with open(ua_json) as f:
    USER_AGENTS = json.load(f)
    
creds_json = f'{ SELENO_DIR }/.env.creds.json'
with open(creds_json) as g:
    DCE_CREDS = json.load(g)


LINES_PER_PAGE = "500"
PORTAL_DDL_PAST_DAYS = 1 
PORTAL_DDL_FUTURE_DAYS = 365 * 5
PORTAL_PUB_PAST_DAYS = 365 * 2
PORTAL_PUB_FUTURE_DAYS = 0

LOADING_TIMEOUT = 1000 * 91
REQ_TIMEOUT = 90
DLD_TIMEOUT = 300

LOG_TIME_FORMAT = '%d/%m-%H:%M:%S'

# PUDATE = "published"
# DDLINE = "deadline"
# REFERE = "reference"
# CATEGC = "category"
# NUMBLO = "lots_count"
# OBJETC = "title"
# LIEUEX = "location"
# ACHETE = "client"
# TYPEAN = "type"
# PROCED = "procedure"
# MODEPA = "mode"
# REPONS = "ebid"
# LOTSSS = "lots"
# PRIXPL = "plans_price"
# DOMAIN = "domains"
# RETDOS = "address_withdrawal"
# DEPOFF = "address_bidding"
# LIEOUV = "address_opening"
# CONTNM = "contact_name"
# CONTML = "contact_email"
# CONTTL = "contact_phone"
# CONTFX = "contact_fax"
# IDENTI = "id"
# LINKKK = "link"
# PORTID = "chrono"
# ACRONY = "acronym"
# LOTNMB = "number"
# OBJETL = "title"
# CATEGL = "category"
# DESCRI = "description"
# ESTIMA = "estimate"
# CAUTIO = "bond"
# RESPME = "reserved"
# QUALIF = "qualifs"
# AGREME = "agrements"
# ECHANT = "samples"
# REUNIO = "meetings"
# VISITS = "visits"
# VARIAN = "variant"
# DCESIZ = "size_read"
# BYTESS = "size_bytes"

# ECHAND = "when"
# ECHANA = "where"
# REUNID = "when"
# REUNIA = "where"
# VISITD = "when"
# VISITA = "where"
# CANCEL = "cancelled"

# RVDATE = 'when'
# RVLIEU = 'where'

NA_PLH = ''
TRUNCA = 32

DL_PATH_PREFIX = 'DCE-'

DCE_CLEANING_DAY = 7        # 1 to 28 (just to be sure)
CLEAN_DCE_AFTER_DAYS = 60
CLEAN_CONS_AFTER_DAYS = 6*365