# ============================================================
# YukiEliteBot | app/keyboards.py
# Purpose: Inline keyboard layouts for the bot interface.
# Version: 1.0.0 | Author: Archon | License: MIT
# ============================================================
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from app.config import SUPPORT_URL,UPDATES_URL,BOT_USERNAME
from app.emojis import emoji

def home():
    add=f"https://t.me/{BOT_USERNAME}?startgroup=true" if BOT_USERNAME else "https://t.me/"
    return InlineKeyboardMarkup([[InlineKeyboardButton(f"{emoji('add')} Add To Your Group",url=add)],[InlineKeyboardButton(f"{emoji('help')} Help",callback_data="help:1"),InlineKeyboardButton(f"{emoji('updates')} Updates",url=UPDATES_URL)],[InlineKeyboardButton(f"{emoji('support')} Support",url=SUPPORT_URL)]])

def help_page(page=1):
    nav=[]
    if page>1: nav.append(InlineKeyboardButton(f"{emoji('prev')} Previous",callback_data=f"help:{page-1}"))
    nav.append(InlineKeyboardButton(f"{page}/3",callback_data="noop"))
    if page<3: nav.append(InlineKeyboardButton(f"Next {emoji('next')}",callback_data=f"help:{page+1}"))
    return InlineKeyboardMarkup([nav,[InlineKeyboardButton(f"{emoji('back')} Back",callback_data="home")]])
