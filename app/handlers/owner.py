# ============================================================
# YukiEliteBot | app/handlers/owner.py
# Purpose: Owner-only broadcast and statistics commands.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
import asyncio
from pyrogram.errors import FloodWait
from app.utils.permissions import is_owner
from app.emojis import emoji
from app.config import BROADCAST_DELAY

async def broadcast(client,message):
    if not message.from_user or not await is_owner(message.from_user.id):return
    if not message.text or len(message.text.split(maxsplit=1))<2:return await message.reply_text("Usage: /broadcast <message>")
    body=message.text.split(maxsplit=1)[1];ids=list(dict.fromkeys(await client.db.ids("users")+await client.db.ids("chats")));sent=failed=0
    status=await message.reply_text(f"{emoji('broadcast')} Broadcast started...\nTargets: <b>{len(ids)}</b>")
    for chat_id in ids:
        try:await client.send_message(chat_id,body);sent+=1;await asyncio.sleep(BROADCAST_DELAY)
        except FloodWait as error:await asyncio.sleep(error.value+1)
        except Exception:failed+=1
    await status.edit_text(f"{emoji('success')} Broadcast finished.\n\n{emoji('success')} Sent: <b>{sent}</b>\n{emoji('error')} Failed: <b>{failed}</b>")

async def stats(client,message):
    if not message.from_user or not await is_owner(message.from_user.id):return
    users,chats,runs,members=await client.db.stats();await message.reply_text(f"{emoji('stats')} <b>Bot Statistics</b>\n\n{emoji('group')} Users: <b>{users}</b>\n{emoji('members')} Chats: <b>{chats}</b>\n{emoji('tag')} Tag runs: <b>{runs}</b>\n{emoji('success')} Members tagged: <b>{members}</b>")
