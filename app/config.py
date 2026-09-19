# ============================================================
# YukiEliteBot | app/config.py
# Purpose: Environment-backed application configuration.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=BASE_DIR/"data"
DATA_DIR.mkdir(exist_ok=True)

def _ints(value):
    return [int(x.strip()) for x in value.split(",") if x.strip().lstrip("-").isdigit()]

BOT_TOKEN=os.getenv("BOT_TOKEN","").strip()
API_ID=int(os.getenv("API_ID","0"))
API_HASH=os.getenv("API_HASH","").strip()
OWNER_IDS=_ints(os.getenv("OWNER_IDS",""))
BOT_USERNAME=os.getenv("BOT_USERNAME","YukiEliteBot").strip().lstrip("@")
SUPPORT_URL=os.getenv("SUPPORT_URL","https://t.me/your_support").strip()
UPDATES_URL=os.getenv("UPDATES_URL","https://t.me/your_updates").strip()
LOG_LEVEL=os.getenv("LOG_LEVEL","INFO").upper()
DB_PATH=os.getenv("DB_PATH",str(DATA_DIR/"yukielite.db"))
TAG_DELAY=max(0.1,float(os.getenv("TAG_DELAY","0.9")))
MENTIONS_PER_MESSAGE=max(1,int(os.getenv("MENTIONS_PER_MESSAGE","6")))
MAX_MEMBERS_PER_SCAN=max(1,int(os.getenv("MAX_MEMBERS_PER_SCAN","50000")))
BROADCAST_DELAY=max(0.05,float(os.getenv("BROADCAST_DELAY","0.08")))
