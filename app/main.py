# ============================================================
# YukiEliteBot | app/main.py
# Purpose: Application bootstrap and Telegram handler registration.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
import logging
from pyrogram import Client,filters
from app.config import BOT_TOKEN,API_ID,API_HASH,LOG_LEVEL
from app.database import Database
from app.services.tagger import TagManager
from app.handlers.start import start_handler
from app.handlers.help import help_command,help_callback
from app.handlers.tagging import tag_command,mention_command,mention_trigger,TAG_COMMANDS
from app.handlers.control import control
from app.handlers.owner import broadcast,stats
from app.handlers.tracking import track

logging.basicConfig(level=getattr(logging,LOG_LEVEL,logging.INFO),format="%(asctime)s | %(levelname)s | yukielite | %(message)s")
if not BOT_TOKEN:raise RuntimeError("BOT_TOKEN is missing")
if not API_ID or not API_HASH:raise RuntimeError("API_ID/API_HASH are missing")
app=Client("yukielite",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)
app.db=Database();app.tagger=TagManager(app,app.db)

@app.on_message(filters.all,group=99)
async def tracker(_,message):await track(app,message)
@app.on_message(filters.command("start",prefixes="/"))
async def start(_,message):await start_handler(app,message)
@app.on_message(filters.command("help",prefixes="/"))
async def help_cmd(_,message):await help_command(app,message)
@app.on_callback_query(filters.regex(r"^(help:\d+|home|noop)$"))
async def help_cb(_,query):await help_callback(app,query)
@app.on_message(filters.command(list(TAG_COMMANDS),prefixes="/"))
async def tags(_,message):await tag_command(app,message)
@app.on_message(filters.command(["admin","all"],prefixes="/"))
async def mentions(_,message):await mention_command(app,message)
@app.on_message(filters.regex(r"^@(admin|all)(?:\s+.*)?$"))
async def at_mentions(_,message):await mention_trigger(app,message)
@app.on_message(filters.command(["stop","pause","resume"],prefixes="/"))
async def controls(_,message):await control(app,message)
@app.on_message(filters.command("broadcast",prefixes="/"))
async def owner_broadcast(_,message):await broadcast(app,message)
@app.on_message(filters.command("stats",prefixes="/"))
async def owner_stats(_,message):await stats(app,message)

async def bootstrap():
    await app.db.init();me=await app.get_me();logging.info("Started @%s (%s)",me.username,me.id)

def run():app.run(bootstrap())
