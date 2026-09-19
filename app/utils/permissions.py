# ============================================================
# YukiEliteBot | app/utils/permissions.py
# Purpose: Telegram owner/admin permission checks.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
from pyrogram.enums import ChatMemberStatus
from app.config import OWNER_IDS

async def is_owner(user_id): return bool(user_id and user_id in OWNER_IDS)
async def is_admin(client,chat_id,user_id):
    try: return (await client.get_chat_member(chat_id,user_id)).status in (ChatMemberStatus.OWNER,ChatMemberStatus.ADMINISTRATOR)
    except Exception: return False
async def bot_is_admin(client,chat_id):
    try: return (await client.get_chat_member(chat_id,"me")).status in (ChatMemberStatus.OWNER,ChatMemberStatus.ADMINISTRATOR)
    except Exception: return False
