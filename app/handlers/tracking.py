# ============================================================
# YukiEliteBot | app/handlers/tracking.py
# Purpose: Discover users and chats for statistics and broadcast.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
async def track(client,message):
    try:
        if message.from_user:await client.db.track_user(message.from_user)
        if message.chat:await client.db.track_chat(message.chat)
    except Exception:pass
