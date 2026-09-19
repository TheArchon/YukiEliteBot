# ============================================================
# YukiEliteBot | app/handlers/start.py
# Purpose: Start command and onboarding.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
from app.keyboards import home
from app.emojis import emoji
from app.utils.formatting import premium_parts

async def start_handler(client,message):
    if message.from_user:await client.db.track_user(message.from_user)
    if message.chat:await client.db.track_chat(message.chat)
    parts=[("bot",emoji("bot"))," <b>YukiEliteBot</b>\n\n",("spark",emoji("spark"))," Fast, clean and professional Telegram tagging.\n\n",("tag",emoji("tag"))," Multiple tagging styles.\n",("pause",emoji("pause"))," Pause, resume or stop active sessions.\n",("vc",emoji("vc"))," Online members first for VC tags.\n\n",("tools",emoji("tools"))," Add me to your group and promote me to administrator for full access."]
    text,entities=premium_parts(parts)
    await message.reply_text(text,entities=entities,reply_markup=home(),disable_web_page_preview=True)
