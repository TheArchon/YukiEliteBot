# ============================================================
# YukiEliteBot | app/utils/telegram.py
# Purpose: Safe Telegram API helpers.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
import asyncio
from pyrogram.errors import FloodWait,RPCError

async def send_safe(client,chat_id,text,**kwargs):
    while True:
        try: return await client.send_message(chat_id,text,**kwargs)
        except FloodWait as error: await asyncio.sleep(error.value+1)
        except RPCError: return None
