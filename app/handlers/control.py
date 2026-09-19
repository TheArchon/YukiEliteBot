# ============================================================
# YukiEliteBot | app/handlers/control.py
# Purpose: Pause, resume and stop active tagging sessions.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
from app.utils.permissions import is_admin
from app.emojis import emoji

async def control(client,message):
    if not message.from_user or not await is_admin(client,message.chat.id,message.from_user.id):return await message.reply_text(f"{emoji('warning')} Only group admins can control tagging.")
    command=message.command[0].lower();ok=await getattr(client.tagger,command)(message.chat.id)
    labels={"stop":("Tagging stopped! All ongoing tagging has been cancelled.","stop"),"pause":("Tagging paused! Use /resume to continue.","pause"),"resume":("Tagging resumed!","resume")}
    if ok:return await message.reply_text(f"{emoji(labels[command][1])} {labels[command][0]}")
    await message.reply_text(f"{emoji('warning')} No active tagging session was found.")
