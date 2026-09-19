# ============================================================
# YukiEliteBot | app/handlers/tagging.py
# Purpose: Tagging and mention command handlers.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
import re
from app.utils.permissions import is_admin,bot_is_admin
from app.emojis import emoji
TAG_COMMANDS={"hitag":"hitag","entag":"entag","gmtag":"gmtag","gntag":"gntag","tagall":"tagall","jtag":"jtag","vctag":"vctag"}

async def _start(client,message,kind,custom=""):
    if str(message.chat.type) not in ("ChatType.GROUP","ChatType.SUPERGROUP","group","supergroup"):return await message.reply_text("Use this command inside a group.")
    if not message.from_user or not await is_admin(client,message.chat.id,message.from_user.id):return await message.reply_text(f"{emoji('warning')} Only group admins can use tagging commands.")
    if not await bot_is_admin(client,message.chat.id):return await message.reply_text(f"{emoji('error')} Please promote me to administrator first.")
    if client.tagger.running(message.chat.id):return await message.reply_text(f"{emoji('warning')} A tagging session is already running!\n\nUse /stop before starting another session.")
    users=await client.tagger.members(message.chat.id,kind)
    if not users:return await message.reply_text(f"{emoji('error')} No eligible members were found.")
    ok,_=await client.tagger.start(message.chat.id,kind,users,custom)
    if ok:await message.reply_text(f"{emoji('start')} Tagging started.\n{emoji('members')} Members found: <b>{len(users)}</b>")

async def tag_command(client,message):await _start(client,message,TAG_COMMANDS[message.command[0].lower()])
async def mention_command(client,message):
    custom=message.text.split(maxsplit=1)[1] if len(message.command)>1 else ""
    await _start(client,message,"admin" if message.command[0].lower()=="admin" else "all",custom)
async def mention_trigger(client,message):
    match=re.match(r"^@(admin|all)(?:\s+(.*))?$",(message.text or "").strip(),re.I)
    if match:await _start(client,message,match.group(1).lower(),match.group(2) or "")
